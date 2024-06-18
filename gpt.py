from openai import OpenAI
import tiktoken
import json

def getToken(file_path, variable):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config.get(variable)

def tokenCnt(messages, model='gpt-4'):
  try:
      encoding = tiktoken.encoding_for_model(model)
      numToken = 0
      for message in messages:
          numToken += 4 
          for key, value in message.items():
              numToken += len(encoding.encode(value))
              if key == "name":  
                  numToken += -1 
      numToken += 2  
      return numToken
  except Exception:
      raise NotImplementedError("""tokenCnt() is not presently implemented for model {model}.""")
      

class GPTManager:
    
    def __init__(self):
        self.chat_history = [] # Stores the entire conversation
        try:
            self.client = OpenAI(api_key=getToken("config.json", "gptToken"))
        except TypeError:
            exit("No OPENAI_API_KEY!")

    # Asks a question with no chat history
    def chat(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        # Check that the prompt is under the token context limit
        question = [{"role": "user", "content": prompt}]
        if tokenCnt(question) > 8000:
            print("The length of this chat question is too large")
            return

        print("\nAsking ChatGPT")
        completion = self.client.chat.completions.create(
          model="gpt-4",
          messages=question
        )

        # Process the answer
        answer = completion.choices[0].message.content
        print("\n{answer}")
        return answer

    # Asks a question that includes the full conversation history
    def chatHistory(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        self.chat_history.append({"role": "user", "content": prompt})

        # Check total token limit.
        print("Current token length of {tokenCnt(self.chat_history)}")
        while tokenCnt(self.chat_history) > 8000:
            self.chat_history.pop(1)
            print("Popped a message! New token length is: {tokenCnt(self.chat_history)}")

        print("Asking ChatGPT")
        completion = self.client.chat.completions.create(
          model="gpt-4",
          messages=self.chat_history
        )

        # Add this answer to our chat history
        self.chat_history.append({"role": completion.choices[0].message.role, "content": completion.choices[0].message.content})

        # Process the answer
        answer = completion.choices[0].message.content
        print("\n{answer}")
        return answer
   

if __name__ == '__main__':
    gptManager = GPTManager()

    while True:
        new_prompt = input("\nNext question?")
        gptManager.chatHistory(new_prompt)
        