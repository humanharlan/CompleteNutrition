# CompleteNutrition
 Using linear algebra to generate nutritionally optimal recipes!

I am interested in nutritionally complete meal products such as Soylent and Huel, and I have often wondered what it would take to cook a meal from scratch that shared the same level of nutritional completeness. To accomplish this, I aim to build an easy-to-use tool that will generate an ingredient list as close as possible to the nutritional make-up of Soylent. I do not have strong opinions about whether the nutritional make-up of Soylent is optimal, I only chose to base my target values on Soylent for the sake of simplicity.

5/6/2021: In its current form, you can manually enter the nutritional information of your ingredients into a command line, and it will calculate the best recipe. Here are some things that need to be improved:

* Make the application pull the nutrition data from a CSV file rather than querying the user
* Right now the least squares solution values daily value of macronutrients and micronutrients equally. I think macronutrients should be weighted more
* Provide more detailed output to the user about the nutritional composition of the generated recipe
* Right now it is possible for the algorithm to choose a negative amount of an ingredient in some edge cases. I need to constrain the solutions to be non-negative
* Create a UI

5/7/2021: I have replaced numpy.lstsq with scipy.nnls so that only non-negative solutions will be used. I also added script to display the nutrition facts of the generated recipe.

5/7/2021: It now reads the ingredient data from ingredients.csv. This is less cumbersome but still involves a lot of data entry. I am considering using the USDA food database to let users lookup nutrition facts, or starting another project for automatic reading of nutrition labels