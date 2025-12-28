from google import genai
import secrets
import subprocess
import os

client = genai.Client(api_key=secrets.api_key)
game_lines = []
game_script = open("game.py", "w")

prompt = input("Please enter game prompt: ")

def write_line(line):
    write_file = open("game.py", "w")
    write_file.writelines(line)
    write_file.close()

def fix_game(code):
    with open("game.py", "r+") as file:
        file.write(code)

    out_file = open("game.py", "r+")
    temp_file = open("temp.py", "w")

    input_lines = out_file.readlines()
    for line in input_lines:
        if not line.strip("\n").startswith("```"):
            temp_file.write(line)

    os.replace("temp.py", "game.py")
    out_file.close()

    out_file.close()


def report_error(error):
    game_file = open("game.py", "r")
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"this code: {game_file.read()}, returned this error: {error}. please fix it. please return only the python script and nothing else. no messages on what you fixed or anything!"
    )
    game_file.close()
    fix_game(response.text)

def run_game():
    try:
        subprocess.check_output(["python", "game.py"])
        subprocess.run(["python", "game.py"])
        with open("game.py", "r") as f:
            feedback(f.read())
    except subprocess.CalledProcessError as e:
        print("game failed to run :(")
        report_error(e.output)
        run_game()

def feedback(game):
    y_n = input("are you satisfied with your game? ([y]es, [n]o): ")
    if y_n == "y":
        y_n = input("would you like to save your game? ([y]es, [n]o): ")
        if y_n == "y":
            game_name = input("please enter game name (no spaces please):")
            game_name = game_name + ".py"
            os.replace("game.py", game_name)
            print("your game has been saved as: " + game_name)
            quit()
        elif y_n == "n":
            print("ok, bye.")
            quit()
        else:
            print("INVALAD CHARACTER! EXITING PROGRAM")
            quit()
    elif y_n == "n":
        y_n = input("would you like to try to improve your game? ([y]es, [n]o): ")
        if y_n == "y":
            new_prompt = input("please tell me what you would like to improve/fix: ")
            print("please wait...")
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"fix this game code: {game}, based on this prompt: {new_prompt}.  please fix it. please return only the python script and nothing else. no messages on what you fixed or anything!"
            )
            fix_game(response.text)
            run_game()
        elif y_n == "n":
            y_n = input("would you like to save your game? ([y]es, [n]o): ")
            if y_n == "y":
                game_name = input("please enter game name (no spaces please):")
                os.replace("game.py", "{game_name}.py")
                print("your game has been saved as: {game_name}.py!")
                quit()
            elif y_n == "n":
                print("ok, bye.")
                quit()
            else:
                print("INVALAD CHARACTER! EXITING PROGRAM")
                quit()
        else:
            print("INVALAD CHARACTER! EXITING PROGRAM")
            quit()
    else:
        print("INVALAD CHARACTER! EXITING PROGRAM")
        quit()


print("please wait...")
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"your response should be only the python script. Generate a simple pygame script based on this prompt: {prompt}.")

fix_game(response.text)

run_game()

