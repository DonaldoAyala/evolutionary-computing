import re

comma_re = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")

countries_variables = {}
countries = set()
variables = set()
max_variables = 0

excluded_countries = {'Greenland', 'Philippines', 'Country Name', 'Puerto Rico'}
excluded_variables = {'Logistics performance index: Overall (1=low to 5=high)', 'Series Name','"Current education expenditure, total (% of total expenditure in public institutions)"'}

with open('countries.csv', 'r') as file:
    while (line := file.readline().rstrip()):
        fields = comma_re.split(line)
        if fields[0] not in countries and fields[0] not in excluded_countries:
            countries.add(fields[0])

with open('variables.csv', 'r') as file:
    while (line := file.readline().rstrip()):
        fields = comma_re.split(line)
        if fields[2] not in variables and fields[2] not in excluded_variables:
            variables.add(fields[2])

with open('data.csv', 'r') as file:
    while (line := file.readline().rstrip()):
        fields = comma_re.split(line)
        if fields[0] in countries and fields[0] not in excluded_countries:
            if fields[2] in variables and fields[-1] != '..':
                if fields[0] not in countries_variables:
                    countries_variables[fields[0]] = {fields[2]}
                else:
                    countries_variables[fields[0]].add(fields[2])


missing_variables = set()
exclude_countries = set()


for key in countries_variables:
    #print(key, "->", len(countries_variables[key]))
    if len(countries_variables[key]) < 12:
        exclude_countries.add(key)
    for variable in variables:
        if variable not in countries_variables[key]:
            missing_variables.add(variable)
            #print("\t", variable, "\n", end="")

#print("Countries with not enough info")
for country in exclude_countries:
    print(country)

#print("Missing variables")
for variable in missing_variables:
    print(variable)

country_features = {}

# Now you have the countries and variables to use
with open('data.csv', 'r') as file:
    while (line := file.readline().rstrip()):
        fields = comma_re.split(line)
        if fields[0] in countries and fields[2] in variables:
            if fields[0] not in country_features:
                country_features[fields[0]] = [fields[1], fields[-1]]
            else:
                country_features[fields[0]].append(fields[-1])

for country in country_features:
    print(country, end=",")
    for value in country_features[country]:
        print(value,sep=",",end=",")
    print()
                