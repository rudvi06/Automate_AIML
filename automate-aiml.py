import csv
import pandas as pd

file_name=input("Enter the csv file to be converted in aiml file : ")
df = pd.read_csv(file_name)

f = open("demo.aiml", "w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<aiml version=\"1.0\">\n")

for index in range(df['intent'].size):
    f.write("<category>\n<pattern>")
    f.write(df.iloc[index]['intent'].upper())
    f.write("</pattern>\n<template>")
    f.write(df.iloc[index]['answer'])
    f.write("</template>\n</category>\n")

f.write("</aiml>")

f.close()
