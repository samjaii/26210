# import needed libraries
from enum import auto
import urllib.parse
import requests
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# Menu definition
def menu():
    print("----------------------------------------")
    print(Fore.MAGENTA + "What would you like to know about \n"+ orig +" to "+ dest +"?")
    print(Fore.BLUE +  "[1]" + Fore.WHITE + " General Info | " + Fore.BLUE +  "[2]" + Fore.WHITE +  " Restrictions")
    print(Fore.BLUE +  "[3]" + Fore.WHITE + " Miscellaneous | " + Fore.BLUE +  "[4]" + Fore.WHITE +  " Directions")
    print(Fore.RED + "[0]" + Fore.WHITE + " Exit Menu")
    print("----------------------------------------")

# Import MapQuest API
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "PJv71zxlt65ihzFpAKRuP6HQ3zaCJDQ9"

print("========================================")
print(Fore.RED + "         " + "MapQuest Pathfinder")
print(Fore.CYAN + "     " + "Developed by Group#8 - 4-ITI")
print("========================================")

while True:
    # Ask user for input regarding starting location & destination
    print("Welcome! Please enter field/s. Use quit/q to end program.")

    orig = input(Style.BRIGHT + "Starting Location: ")
    if orig == "quit" or orig == "q":
        print("========================================")
        print(Fore.GREEN + "Thank you for using MapQuest Pathfinder!")
        break
    dest = input(Style.BRIGHT + "Destination: ")
    if dest == "quit" or dest == "q":
        print("========================================")
        print(Fore.GREEN + "Thank you for using MapQuest Pathfinder!")
        break
    
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})

    # Get json data request
    json_data = requests.get(url).json()

    print("----------------------------------------")
    print("URL " + (url))
    print("----------------------------------------")

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    # Output if successful json route call
    if json_status == 0:
        print("API Status " + str(json_status) + " = Congratulations! A successful route call.\n")
        # Options
        menu()
        loop = 1
    
        while loop == 1:
            # Ask user for option number from menu
            option = (input(Fore.CYAN +"Please enter your option: "))

            if option == "1":
                print("SELECTED: General Info")
                print("Trip Duration: " + (json_data["route"]["formattedTime"]) + " \n")
                
                distMi = (json_data["route"]["distance"])
                # Distance conversion
                distKm = (json_data["route"]["distance"])*1.61
                distM = (json_data["route"]["distance"])*1609.344
                
                print("Distance: ")
                print("(in mi): " + str("{:.2f}".format(distMi)) + " mi")
                print("(in km): " + str("{:.2f}".format(distKm)) + " km")
                print("(in m): " + str("{:.2f}".format(distM)) + " m \n")
                
                menu()
            elif option == "2":
                print("SELECTED: Restrictions")
                print("Timed restriction: " + str(json_data["route"]["hasSeasonalClosure"]))
                print("Seasonal closure: " + str(json_data["route"]["hasSeasonalClosure"]))
                print("Country cross: " + str(json_data["route"]["hasCountryCross"]))
                
                menu()
            elif option == "3":
                print("SELECTED: Miscellaneous")
                print("Has toll road: " + str(json_data["route"]["hasTollRoad"]))
                print("Has tunnel: " + str(json_data["route"]["hasTunnel"]))
                print("Has highway: " + str(json_data["route"]["hasHighway"]) + "\n")
                
                # Geo Quality Code
                print("Geo Quality Code of " + orig + ": " + (json_data["route"]["locations"][0]["geocodeQualityCode"]))
                print("Geo Quality Code of "+ dest + ": " + (json_data["route"]["locations"][1]["geocodeQualityCode"]))

                menu()
            elif option == "4":
                print("SELECTED: Directions")
                for each in json_data["route"]["legs"][0]["maneuvers"]:
                    print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
                
                menu()
            elif option == "0":
                loop = 0
                print(Fore.GREEN + "Thank you for using the menu.")
                print("----------------------------------------")
            else:
                print(Fore.RED + "Oops! Invalid option. Please choose a number from the menu.")
                menu()

    # Output if unsuccessful json route calls
    elif json_status == 402:
        print("****************************************")
        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("****************************************")
    elif json_status == 611:
        print("****************************************")
        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("****************************************")
    elif json_status == 500: # Added status code 500
        print("****************************************")
        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; The server encountered an error and could not complete your request.")
        print("****************************************")
    elif json_status == 404: # Added status code 404
        print("****************************************")
        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; The resource addressed by the request URL does not exist.")
        print("****************************************")
    else:
        print("****************************************")
        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "For Status Code: " + str(json_status) + "; Refer to:")
        print(Fore.RED + "https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("****************************************\n")