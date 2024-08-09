import argparse
import requests

def main():
    parser = argparse.ArgumentParser(description="User search for the Art Institute of Chicago API")
#Flags
    group = parser.add_argument_group('Search options')
    oGroup = parser.add_argument_group('Aditional flags')
    group.add_argument("--id", help ="Search an artwork using a numeric id")
    group.add_argument("-s","--search", help="Search all artworks that contain user query")
    oGroup.add_argument("-f","--fields", nargs='+', help="Fields that the user wants to get after their query comma separated")
    group.add_argument("-p","--page", help="Search for the artworks starting on user input page number, can also be used as a flag for search")
    oGroup.add_argument("-l","--limit", help="Limits the ammount of results the user is getting")

    args = parser.parse_args()
    url = "https://api.artic.edu/api/v1/artworks"
    parameters = {'fields':args.fields}
    query = {'q':args.search,'fields':args.fields,'page':args.page,'limit':args.limit}
#Querys
    response = ""
    if args.id and not (args.search or args.limit or args.page):
        response = requests.get(url + "/" + args.id, params = parameters)  
    elif not args.id and (args.page or args.limit):
        response = requests.get(url + "/search", params = query)
    else:
        print("invalid search try again")

#File writing 
    file = open("Query.pdf","w")
    if(response and response.status_code == 200): 
        fields = response.json()['data']   
        file.write("Welcome, your results are: \n")
        file.write("\n")
        if (type(fields) == dict): 
            for field in fields:
                file.write(f"{field}: {fields[field]} \n")
        elif (type(fields) == list): 
            for item in fields:
                for key, value in item.items():
                    file.write(f"{key}: {value} \n")
                file.write("---------------------------------------\n")        
    else:
        file.write("Your search did not return any results")
    file.close()
    
if __name__ == '__main__':
    main()

