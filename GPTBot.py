# coding: utf-8
# Autor: Gustavo Gonçalves
# Data: 01/02/2023

import openai, telebot

print("BOT INICIADO");

class TGBot:
    def __init__(self):
        self.sk = {"GPT":"SUA SECRET KEY GPT AQUI", "TG":"SUA SECRET KEY DO TELEGRAM AQUI (BotFather)"};
        self.bot = telebot.TeleBot(self.sk["TG"]);
    
    def sendMsg(self, chatId, msg, parse_mode = "MarkDown"):
        self.bot.send_message(chatId, msg); 
        #Bot envia msg
    
    def editMsg(self, chatId, msg, msgId, parse_mode = "MarkDown"):
        self.bot.edit_message_text(chat_id = chatId, text = msg, message_id = msgId);
        #Bot edita a própria msg
        
    def gpt(self, msg):
        openai.api_key = self.sk['GPT'];
        result = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = [{"role": "user", "content": msg}], max_tokens = 2048, temperature = 0.8);
        return(result.choices[0].message.content);
        #api do gpt para gerar respostas
    
    def dall_e(self, msg):
        openai.api_key = self.sk['GPT'];
        result = openai.Image.create(prompt = msg, n = 1, size = "512x512");
        return(result["data"][0]["url"]);
        #api do dall-e para gerar imagens

    def getMsg(self, msg):
        for m in msg:
            self.chatId = m.chat.id;
            self.msgId = m.message_id;
            if m.content_type == "text":
                text = m.text;
                
                #Inicio dos comandos aqui
                if text.startswith("/gpt"): #comando /gpt "exemplo" no chat
                    self.cmd = text[len('/gpt '):];
                    self.sendMsg(self.chatId, "Gerando resposta...");
                    self.editMsg(self.chatId, self.gpt(self.cmd), self.msgId+1, parse_mode = "HTML");
                elif text.startswith("/img"): #comando /img "descrição" no chat
                    self.cmd = text[len('/img '):];
                    self.sendMsg(self.chatId, "Gerando imagem...");
                    self.editMsg(self.chatId, self.dall_e(self.cmd), self.msgId+1, parse_mode = "HTML");
                #fim dos comandos aqui 

    def main(self):
        self.bot.set_update_listener(self.getMsg); 
        self.bot.polling();

if __name__ == "__main__":
    tgBot = TGBot();
    tgBot.main();