# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:04:51 2020

@author: mak80
"""
import random
import sys
import pandas as pd 

''' Class player for storing player cards '''
class Player:
    ''' Create palyer - name , cards, fold_count '''
    def __init__(self, name):
        print("Player "+ name +" ready")
        self.player = name
        self.cards = None
        self.fold_count = 0
    
    ''' player draw cards '''
    def draw_cards(self, cards):
        self.cards = cards
    
    ''' return player cards '''
    def view_cards(self):
        return print(self.cards)
    
    ''' return player name '''
    def get_name(self):
        return(self.player)
    
    ''' Fold the cards '''
    def fold(self):
        self.cards = None
        self.fold_count+=1
        return

    ''' Give cards back to croupier '''
    def give_cards_back(self):
        self.cards = None
        return
    
''' Class for dealing with the deck'''
class Croupier:
    
    ''' Create space for dack and top card tracker '''
    def __init__(self):
        self.deck = self.create_deck()
        self.top_card_id = 0
        
    ''' Draw cards for player '''
    def deal_cards_to_player(self):
        player_cards = (self.draw_card(), self.draw_card())
        return player_cards
    
    ''' Function for drwaing a card '''
    def draw_card(self):
        card = self.deck.get(self.top_card_id)
        self.top_card_id += 1
        return card
    
    ''' Function for card burning '''
    def burn_card(self):
        self.top_card_id += 1
    
    ''' Function to create new deck '''
    def create_deck(self):
        self.cards = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.colours = ['c','d','h','s']
        deck = {}
        for i in range(0, len(self.colours)):
            for k in range(0, len(self.cards)):
                card = self.cards[k]+self.colours[i]
                deck[len(deck)]=card
        random.shuffle(deck)
        return deck
    
    ''' Draw 3 cards '''
    def drwa_flop(self):
        self.burn_card()
        self.burn_card()
        self.flop = []
        for i in range(0,3):
            self.flop.append(self.draw_card())
        return self.flop
    
    ''' Cropier decides who won '''
    def decide_who_won(self, p1, p2):
        
        ''' Memory to store winner cards '''
        winner = 0
        
        ''' Scores of both players '''
        score1 = self.check_player_combination(p1.cards)
        score2 = self.check_player_combination(p2.cards)
        print('Player score : ', score1)
        print('Ai score : ', score2)
        
        ''' Loop to decide on winnner '''
        for i in range(0, len(score1)):
            if score1[i]>score2[i]:
                print(p1.player,' is the winner')
                winner = p1.cards
                break
            elif score1[i]<score2[i]:
                print(p2.player, ' is the winner')
                winner = p2.cards
                break
        return winner
    
    ''' Check players combinations and high cards '''
    def check_player_combination(self, cards):
        
        ''' Define possible combinations '''
        high_card = False
        pair = False
        double_pair = False
        triple = False
        straight = False
        flush = False
        full_house = False
        quads = False
        royal_flush = False
        poker = False
        
        ''' Memory to store combination score '''
        score = [0]
        
        ''' array 5 cards to check '''
        cards_to_check = self.flop
        cards_to_check.append(cards[0])
        cards_to_check.append(cards[1])
        
        
        ''' Create df and set cards from table to data frame '''
        df = pd.DataFrame(0, index=self.colours, columns=self.cards)
    
        for card in cards_to_check:
            df[str(card[:-1])][str(card[-1])] = 1
        
        ''' Sum up colours and values'''
        values = df.sum(axis=0)
        colours = df.sum(axis=1)
        
        ''' Check for flush '''
        for each in colours:
            if each > 4:
                flush = True
                if score[0] < 5:
                    score = [5]
        ''' Check for other combinations'''
        straight_count = 0
        for each in values:
            '''double pair'''
            if each == 2 and pair == True:
                double_pair = True
                if score[0] < 2:
                    score = [2]
            ''' quads '''
            if each == 4:
                quads = True
                if score[0] < 7:
                    score = [7]
            ''' triple '''
            if each == 3:
                triple = True
                if score[0] < 3:
                    score = [3]
            ''' pair '''
            if each == 2:
                pair = True
                if score[0] < 1:
                    score = [1]
            ''' full_house '''    
            if triple == True and pair == True:
                full_house == True
                if score[0] < 6:
                    score = [6]
            ''' straight '''
            if each == 1:
                straight_count += 1
            if straight_count == 5:
                straight = True
                if score[0] < 4:
                    score = [4]
            if each == 0:
                straight_count = 0
        ''' royal_flush '''
        if straight == True and flush == True:
            royal_flush = True
            if score[0] < 8:
                score = [8]
            ''' poker '''
            if values == [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]:
                poker = True
                if score[0] < 9:
                    score = [9]
        ''' high card '''
        if score[0] == 0:
            high_card = True
        
        ''' Decide on high card sequence'''
        if royal_flush == True:
            for i in range(12, -1 ,-1):
                if values[i]>0:
                    score.append(i)
        if full_house == True:
            for i in range(12, -1 ,-1):
                if values[i]>2:
                    score.append(i)
            for i in range(12, -1 ,-1):
                if values[i]>1:
                    score.append(i)
        if pair == True or double_pair == True:
            for i in range(12, -1 ,-1):
                if values[i]>1:
                    score.append(i)
            for i in range(12, -1 ,-1):
                if values[i]>0:
                    score.append(i)
        if straight == True:
            for i in range(12, -1 ,-1):
                if values[i]>0:
                    score.append(i)
        if triple == True:
            for i in range(12, -1 ,-1):
                if values[i]>2:
                    score.append(i)
            for i in range(12, -1 ,-1):
                if values[i]>1:
                    score.append(i)
            for i in range(12, -1 ,-1):
                if values[i]>0:
                    score.append(i)
        if quads == True:
            for i in range(12, -1 ,-1):
                if values[i]>3:
                    score.append(i)
        if flush == True:
            for i in range(12, -1 ,-1):
                if values[i]>0:
                    score.append(i)
        if high_card == True:
            for i in range(12, -1 ,-1):
                if values[i]>0:
                    score.append(i)
        
        '''Empty variables'''
        cards_to_check.remove(cards[0])
        cards_to_check.remove(cards[1])
        
        return score
    
        
''' Class which stands for table, sapce seen by both players '''
class Table:
    ''' Space for player cards and flop '''
    def __init__(self):
        self.p1_cards = ()
        self.p2_cards = ()
        self.cards_on_table = []

    ''' Show cards on table '''
    def view_table(self):
        print(self.p1_cards)
        print(self.cards_on_table)
        print(self.p2_cards)
        return
    
    ''' Draw cards to table '''
    def get_flop(self, flop):
        self.cards_on_table = flop
        return
    
    ''' Future work 'river' and 'turn' cards '''
    def get_next_card(self, card):
        self.cards_on_table.append(card)
        return
    
    ''' Cleans cards from the table '''
    def clean_table(self):
        self.p1_cards = ()
        self.p2_cards = ()
        self.cards_on_table = []
        return
        
    
''' Class to control the main of the game '''
class Game:
    ''' Start Game '''
    def __init__ (self):
        ''' Create players '''
        print("Type in your name")
        player = Player(input())
        ai = Player("Ai")
        
        while (1):
            ''' Create Table and Croupier '''
            croupier = Croupier()
            table = Table()
            
            ''' Deal cards to players '''
            player.draw_cards(croupier.deal_cards_to_player()) 
            ai.draw_cards(croupier.deal_cards_to_player())
            
            ''' View player cards '''
            player.view_cards()
            
            ''' Show Flop on the table '''
            table.get_flop(croupier.drwa_flop())
            table.view_table()
        
            ''' Fold or not '''
            while player.fold_count < 5:
                a = input("Please Type 'Yes' to fold or 'No' not to fold: ")
                if a == "Yes" or a == "yes":
                    if player.fold_count<4: 
                        ''' Player fold - new table '''
                        player.fold()
                        ai.give_cards_back()
                        fold_count = 5 - player.fold_count
                        print("You can still fold ", fold_count, " times.")
                        break
                    else:
                        ''' Player not fold - Determinate who is winning '''
                        print("You have exceeded the upper limit")
                        table.p1_cards = player.cards
                        table.p2_cards = ai.cards
                        table.view_table()
                        
                        ''' Write to file '''
                        f = open("pokerhandhistory.txt","a")
                        f.write(str(player.player) + ' : ' + str(player.cards) + '. ' + str(ai.player) +' : '+ str(ai.cards) + '. Floop: ' + str(table.cards_on_table) + '. \n')
                        f.close
                        
                        ''' Decide who won '''
                        winner = croupier.decide_who_won(player, ai)
                        print(winner)
                        
                        ''' End Game ''' 
                        self.end_game() 
                        
                if a == "No" or a == "no":
                    ''' Player not fold - Determinate who is winning '''
                    table.p1_cards = player.cards
                    table.p2_cards = ai.cards
                    table.view_table()
                    
                    ''' Write to file '''
                    f = open("pokerhandhistory.txt","a")
                    f.write(str(player.player) + ' : ' + str(player.cards) + '. ' + str(ai.player) +' : '+ str(ai.cards) + '. Floop: ' + str(table.cards_on_table) + '. \n')
                    f.close
                    
                    ''' Decide who won '''
                    winner = croupier.decide_who_won(player, ai)
                    print(winner)
                    
                    ''' End Game ''' 
                    self.end_game()   
                    
    ''' Exit Game '''
    def end_game(self):
        sys.exit()
        
def main():
    ''' Start of the program '''
    while (1):
        print("Please Type 'Start' to start or 'End' to end")
        a = input()
        if a == "Start" or a == "start":
            Game()
        if a=="End" or a =="end":
            sys.exit()

main()