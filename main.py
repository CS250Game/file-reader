import json

file = open("C:/Users/gbell/OneDrive/Desktop/SNHU/Fall-2023/SDLC/Project/dbf84c87-9967-3dcc-857c-cb206907df92.json")

minecraftData = json.load(file)

for i in minecraftData:
   print(i)

#Find out what stats we want to display and pull those into variables
#Push those stats to DB