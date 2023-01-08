class Category:
  #constructor  
  def __init__(self, category):
    self.category = category
    self.ledger = list()
    self.balance = 0
  
  #creating the output  
  def __str__(self): 
  #title row
    title = self.category
    #line should be 30 characters, and the name should be centered
    star_length = (30 - len(title)) / 2
    #creating a loop to get the right number of stars
    i = 0
    stars = ""
    while i < star_length:
      stars += "*"
      i += 1
    #stars and name together  
    ledger_title = stars + title + stars
    rows = ""
    total = 0
    #iterating through each pair in the ledger list
    for row in self.ledger: 
      #using {[argument_index_or_keyword]:[width][.precision][type]}
      item_desc = f"{row['description'][0:23]:23s}" 
      item_amount = f"{row['amount']:7.2f}" 
      #how much space goes in between description and amount to right align it
      spacing = 30 - len(item_desc) - len(item_amount)
      right_adjust = ""
      j = 0
      while j < spacing:
        right_adjust += " "
        j += 1
      #build each row  
      rows += item_desc + right_adjust +  item_amount + '\n'
      #calculate total
      total += row['amount']
    output = ledger_title + '\n' + rows + "Total: " + str(total)
    return output
    
  #deposit
  def deposit(self, amount, description=""):
    newDep = {"amount": amount, "description": description}
    self.ledger.append(newDep)
    self.balance += amount

  #withdraw
  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      amount = 0 - amount
      newWith = {"amount": amount, "description": description}
      self.ledger.append(newWith)
      self.balance += amount 
      return True
    else:
      return False

  #get_balance
  def get_balance(self):
    return self.balance

  #transfer
  def transfer(self, amount, category):
    if self.check_funds(amount):
      amount_out = 0 - amount
      description_out = "Transfer to " + category.category
      amount_in = amount 
      description_in = "Transfer from " + self.category
      add_to_ledger = {"amount": amount_out, "description": description_out}
      self.ledger.append(add_to_ledger)
      self.balance += amount_out
      new_category_ledger = {"amount": amount_in, "description": description_in}
      category.ledger.append(new_category_ledger)
      category.balance += amount
      return True
    else:
      return False

  #check_funds
  def check_funds(self, amount):
    if amount > self.balance:
      return False
    else:
      return True

#creating the bar chart 
def create_spend_chart(categories):
  spent_totals = [] #list of totals for each category
  cat_names = []
  for category in categories:
    cat_names.append(category.category)
    spent_amt = 0
    #goes through each item in the ledger
    for item in category.ledger:
      #if the value of the amount is less than zero (spent money)
      if item["amount"] < 0:
        spent_amt += int(abs(item["amount"]))
    spent_totals.append(spent_amt) 
    
  #calculate percentage
    #fix this area!! 
  grand_total = round(sum(spent_totals), 2)
  percents = []
  x = 0
  while x < len(spent_totals):
    percent = round((spent_totals[x] / grand_total), 2) * 100
    #rounding down to nearest 10
    percent = str(percent).split(".")[0]
    if int(percent) < 10:
      percent = "0"
    elif int(percent) < 100:
      percent = str(percent)[0] + "0"
    percents.append(percent)
    x += 1

  chart_title = "Percentage spent by category"
  #creating each part of the grid as a list to use for loops later during chart compilation
  y_axis = []
  big_list= [[] for i in range(len(cat_names))]
  grid = 100
  while grid >= 0:
    y_axis.append(str(grid) + "|")
    grid -= 10
  for name in range(len(cat_names)):
    for line in range(len(y_axis)): 
      if y_axis[line].startswith(percents[name]) and len(y_axis[line]) < 4 :
          big_list[name].append(" o ")
          break
      else:
          big_list[name].append("   ")
  for name in range(len(cat_names)):
    i = 11 - (len(big_list[name]))
    while i > 0 :
      big_list[name].append(" o ")
      i -= 1

   
  #making the labels the same length
  longest = 0 
  for category in categories: 
    if len(category.category) > longest:
     longest = len(category.category)
  for x in range(len(categories)):
    cat_names[x] = cat_names[x].ljust(longest)
  
  labels = ""
  for x in range(longest):
    labels += " " * 5
    for category in cat_names:
      labels += category[x] + "  "
    if x != longest-1:
      labels += '\n'
  
  #add title
  chart = chart_title + '\n'
  #define x-axis length
  x_axis = " " * 4
  for i in range(len(cat_names)):
    x_axis += "---" 
  
  #add grid
  for i in range(len(y_axis)):
    if len(y_axis[i]) == 2:
      chart += "  "
    elif len(y_axis[i]) == 3:
      chart += " "
    chart += y_axis[i]
    for y in range(len(cat_names)):
      chart += big_list[y][i]     
    chart += " " + '\n'
 #add dashes(x-axis)
  chart += x_axis + "-" +  '\n'
 #add labels
  chart += labels

  return chart
