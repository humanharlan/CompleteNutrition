import numpy as np
from scipy.optimize import nnls
import csv

nutrients = ["fat", "sodium", "carbs", "protein", "fiber", "vitD",
             "calcium", "iron", "potassium", "vitaminA", "vitaminC", "vitaminE",
             "vitaminK", "thiamine", "riboflavin", "niacin", "vitaminB6",
             "folate", "vitaminB12", "biotin", "pantothenicAcid", "phosphorus",
             "iodine", "magnesium", "zinc", "selenium", "copper", "manganese",
             "chromium", "molybdenum", "chloride", "choline"]

#a list of target values for the different nutrients, turned into a matrix
targets = np.array([40, 25, 14, 15, 40, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                    20, 20, 20, 20, 20, 20, 50, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], dtype = 'float')

# takes a list and index, puts a dictionary that represents ingredient in the list at index
def inputIngredient(ingredients, index):
    ingredient={} #create a dictionary for this ingredient
    print("~New Ingredient~\n")
    ingredient["ID"] = index
    ingredient["Name"] = input("Enter the name of the ingredient\n")
    ingredient["Unit"] = input("Enter the name of the units\n")
    ingredient["Serving"] = float(input("Enter the serving size\n"))
    #Calorie input is divided by 10 to give it more balanced weighting with the other parameters
    ingredient["Calories"] = (float(input("Enter the number of calories\n"))/10)

    for nutrient in nutrients:
        ingredient[nutrient] = float(input("Enter the %DV of " + nutrient + "\n"))

    ingredients.append(ingredient)

#reads a csv file and adds it to a list
def readIngredient(ingredients, file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["Calories"] = float(row["Calories"])/10
            ingredients.append(row)

#get the data from the user. TODO: add automatic data extraction from a database

numberOfIngredients = 0
choice = "N"
ingredientList = []

#Loop to add ingredients until user chooses to calculate recipe

#while (choice != "C"):
#    inputIngredient(ingredientList, numberOfIngredients)
#    numberOfIngredients += 1
#    choice = input("\n(N)ew Ingredient\n(C)alculate Recipe\n")

readIngredient(ingredientList, "ingredients.csv")

#Calculate a recipe

print("\nCalculating recipe...\n")

#a list to store lists of nutrient values
values = []

for ingredient in ingredientList:
    #Turn all of the ingredient data into a list
    ingredientValues=list(ingredient.values())
    #get rid of the first four entries so it's just the nutrient values
    ingredientValues.pop(0) 
    ingredientValues.pop(0)
    ingredientValues.pop(0)
    ingredientValues.pop(0)
    values.append(ingredientValues) #add this list to the list-of-lists "values" 

#turn the list-of-lists into a numpy 2d array
nutrientMatrix = np.array(values, dtype = 'float') 

#find the least squares solution. ".T" creates the transpose of our nutrientMatrix,
#which makes rows=nutrient and columns=ingredient
solution, residual = nnls(nutrientMatrix.T, targets)

print("\nIngredients:\n")

#print the amount of each ingredient greater than 0
for i in range(0, len(solution)):
    if (solution[i]>0):
        print("\n" + str((solution[i]*float(ingredientList[i]["Serving"]))) + " " +
              str(ingredientList[i]["Unit"]) + " of " + str(ingredientList[i]["Name"]))

#populate a list of nutrition facts for the recipe by summing the
#nutrition facts of each ingredient multiplied by its quantity
recipeNutritionFacts = []
for i in range(0,32):
    sum = 0
    for j in range (0, len(values)):
        sum += (float(values[j][i]) * solution[j])
    recipeNutritionFacts.append(sum)
    

print("Residual (smaller number is closer to target nutrition): ")
print(residual)

#Calculate and print out the nutrition facts for the recipe
print("\nNutrition Facts:")
print("\nCalories: " + str(recipeNutritionFacts[0]*10))
for i in range(1, 32):
    print("\n" + nutrients[i-1] + ": " + str(recipeNutritionFacts[i]) + " %DV")

