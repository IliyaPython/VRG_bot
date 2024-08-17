import g4f

g4f.debug.logging = False  # enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # check version
print(g4f.Provider.Ails.params)  # supported args

# # Automatic selection of provider

# # streamed completion
# response = g4f.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "Hello"}],
#     stream=True,
# )

# for message in response:
#     print(message, flush=True, end="")

# # normal response
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     messages=[{"role": "user", "content": "Hello"}],
# )  # alternative model setting

messages = []

while True:
    # Get user input
    user_input = input("You: ")
    
    # Check if the user wants to exit the chat
    if user_input.lower() == "exit":
        print("Exiting chat...")
        break  # Exit the loop to end the conversation

    # Update the conversation history with the user's message
    messages.append({"role": "user", "content": user_input})

    try:
        # Get GPT's response
        response = g4f.ChatCompletion.create(
            messages=messages,
            model=g4f.models.gpt_4,
        )

        # Extract the GPT response and print it
        gpt_response = response
        print(f"Bot: {gpt_response}")

        # Update the conversation history with GPT's response
        messages.append({"role": "assistant", "content": gpt_response})
    except Exception as e:
        print(f"An error occurred: {e}")