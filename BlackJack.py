from random import shuffle

from Card import Card

from Robot import Robot


def jqk(Card):
    if Card.rank == "Jack" or Card.rank == "Queen" or Card.rank == "King":
        return 10
    elif Card.rank is not "Ace":
        return Card.rank
    else:
        return 0

def game():
    cards = []
    money = 100
    bet = 1
    #win pays 3:2 while blackjack pays 2:1

    for i in range(4):
        if i == 0:
            type = "Hearts"
        elif i == 1:
            type = "Diamonds"
        elif i == 2:
            type = "Clubs"
        elif i == 3:
            type = "Spades"
        for j in range (1, 14):
            if j == 1:
                c = Card("Ace", type)
            elif j == 11:
                c = Card("Jack", type)
            elif j == 12:
                c = Card("Queen", type)
            elif j == 13:
                c = Card("King", type)
            else:
                c = Card(j, type)
            cards.append(c)

    shuffle(cards)

    cardcounter = 0
    while True:
        if money <= 0:
            while True:
                print("Looks like you're in the hole.\n\n1.Call loanshark\n2.Exit game")
                ui = raw_input()
                if ui == '1':
                    money += 100
                    break
                elif ui == '2':
                    exit()
                else:
                    print("Don't think you can get out of this one!")
        if cardcounter >= 52:
            print("Full deck has been used, reshuffling the cards.")
            cardcounter = 0
            shuffle(cards)
        dealer1 = cards.pop()
        player1 = cards.pop()
        dealer2 = cards.pop()
        player2 = cards.pop()
        cardcounter += 4
        pcards = []
        dcards = []
        pcards.append(player1)
        pcards.append(player2)
        dcards.append(dealer1)
        dcards.append(dealer2)
        psum = 0
        dsum = 0
        pace = False
        dace = False
        psum += jqk(player1)
        psum += jqk(player2)
        dsum += jqk(dealer1)
        dsum += jqk(dealer2)
        if player1.rank == "Ace" and player2.rank == "Ace":
            psum = 2
        elif player1.rank == "Ace" or player2.rank == "Ace":
            pace = True
            psum += 11
        if dealer1.rank == "Ace" and dealer2.rank == "Ace":
            dsum = 2
        elif dealer1.rank == "Ace" or dealer2.rank == "Ace":
            dace = True
            dsum += 11
        print("\nDealer has a " + str(dealer2.rank) + " of " + dealer2.type + " and another card.\n")
        print("You have a " + str(player1.rank) + " of " + player1.type + " and a " + str(player2.rank) + " of " + player2.type)
        print("\nMoney: " + str(money) + "\nBet: " + str(bet))
        if psum == 21:
            print("Blackjack! You win!")
            money += bet * 2
            continue
        while True:
            bust = False
            print("\nOptions\n1.Hit\n2.Stand\n3.View Cards\n4.Increase Bet\n5.Exit")
            choice = raw_input()

            if choice == "1":
                card = cards.pop()
                out = 0
                cardcounter += 1
                pcards.append(card)
                psum += jqk(card)
                print("\nYou draw a " + str(card.rank) + " of " + card.type)
                if card.rank == "Ace":
                    if psum + 11 > 21:
                        psum += 1
                    else:
                        psum += 11
                        pace = True
                if pace and psum > 21:
                    psum -= 10
                    pace = False
                if psum > 21:
                    print("\nYou bust with " + str(psum) + " against dealers " + str(dsum) + ". Better luck next time.")
                    money -= bet
                    out = 1
                elif psum < 21:
                    print("You now have ")
                    for card in pcards:
                        print(str(card.rank) + " of " + card.type)
                    continue
                else:
                    print("\nBlackjack! You win!")
                    money += bet * 1.5
                    out = 1
                if out == 1:
                    out = 0
                    for card in pcards:
                        cards.insert(0, card)
                    for card in dcards:
                        cards.insert(0, card)
                    break

            elif choice == "2":
                step = False
                print("\nDealer has a " + str(dealer2.rank) + " of " + dealer2.type + " and a " + str(dealer1.rank) + " of " + dealer1.type)
                if dsum > psum:
                    print("\nDealer wins with " + str(dsum) + " against your " + str(psum))
                    money -= bet
                    break
                while dsum < 17:
                    step = True
                    card = cards.pop()
                    cardcounter += 1
                    dsum += jqk(card)
                    dcards.append(card)
                    if card.rank == "Ace":
                        if dsum + 11 <= 21:
                            print("ace less than 21")
                            dsum += 11
                        else:
                            print("ace greater than 21")
                            dsum += 1
                        dace = True
                    #print("\n\ndsum = " + str(dsum) + "\n\n")
                    print("\nDealer drew a " + str(card.rank) + " of " + card.type)
                    print("\nDealer now has \n")
                    for card in dcards:
                        print(str(card.rank) + " of " + card.type)
                    if dsum > 21 and not dace:
                        print("Dealer busts with " + str(dsum) + ". You win!")
                        money += bet * 1.5
                        bust = True
                        break
                    elif dsum > 21 and dace:
                        dsum -= 10
                        dace = False
                    elif dsum <= 21 and dsum > psum:
                        print("\nDealer wins with " + str(dsum) + " against your " + str(psum) + ". Better luck next time.")
                        money -= bet
                        bust = True
                        break
                    elif dsum >17 and dsum == psum:
                        print("\nBoth of you have " + str(dsum) + ". You break even.")
                        bust = True
                        break
                if step == False and dsum < 22 and dsum > 17 and dsum > psum:
                    print("\nDealer wins with " + str(dsum) + " against your " + str(psum) + ". Better luck next time.")
                    money -= bet
                elif dsum < psum:
                    print("\nYou win with " + str(psum) + " against dealer's " + str(dsum))
                    money += bet * 1.5
                elif dsum == psum:
                    print("\nBoth of you have " + str(psum) + ". You break even.")
                for card in pcards:
                    cards.insert(0, card)
                for card in dcards:
                    cards.insert(0, card)
                break
            elif choice == "3":
                print("\nDealer has " + str(dealer2.rank) + " of " + dealer2.type + "\nYou have \n")
                for card in pcards:
                    print(str(card.rank) + " of " + card.type)
            elif choice == "4":
                newbet = 0
                while True:
                    newbet = raw_input("Please enter your new bet\n")
                    if float(newbet) > money:
                        print("You don't have that much money!\n")
                    else:
                        bet = float(newbet)
                        break
            elif choice == "5":
                exit()
            else:
                print("Try again")

        user = raw_input("\nContinue? Y/N\n")
        while True:
            if user == "N":
                exit()
            if user == "Y":
                print("\nOK!")
                break
            else:
                print("\nNot a choice. Try again.")
            if bust:
                break









#robot game playing
#this is not yet complete

def roboGame(Robot):
    while True:
        print("You will watch the robot play. Press 1 to continue each time.\n")
        ui = raw_input()
        if ui == "1":
            break
        else:
            print("That's not a choice!")
    cards = []
    money = 100
    bet = 1
    #win pays 3:2 while blackjack pays 2:1

    for i in range(4):
        if i == 0:
            type = "Hearts"
        elif i == 1:
            type = "Diamonds"
        elif i == 2:
            type = "Clubs"
        elif i == 3:
            type = "Spades"
        for j in range (1, 14):
            if j == 1:
                c = Card("Ace", type)
            elif j == 11:
                c = Card("Jack", type)
            elif j == 12:
                c = Card("Queen", type)
            elif j == 13:
                c = Card("King", type)
            else:
                c = Card(j, type)
            cards.append(c)

    shuffle(cards)

    cardcounter = 0
    User = ""
    while User == "1":
        if money <= 0:
            while True:
                print("Looks like you're in the hole.\n\n1.Call loanshark\n2.Exit game")
                ui = raw_input()
                if ui == '1':
                    money += 100
                    break
                elif ui == '2':
                    exit()
                else:
                    print("Don't think you can get out of this one!")
        if cardcounter >= 52:
            print("Full deck has been used, reshuffling the cards.")
            cardcounter = 0
            shuffle(cards)
        dealer1 = cards.pop()
        player1 = cards.pop()
        dealer2 = cards.pop()
        player2 = cards.pop()
        cardcounter += 4
        pcards = []
        dcards = []
        pcards.append(player1)
        pcards.append(player2)
        dcards.append(dealer1)
        dcards.append(dealer2)
        psum = 0
        dsum = 0
        pace = False
        dace = False
        psum += jqk(player1)
        psum += jqk(player2)
        dsum += jqk(dealer1)
        dsum += jqk(dealer2)
        if player1.rank == "Ace" and player2.rank == "Ace":
            psum = 2
        elif player1.rank == "Ace" or player2.rank == "Ace":
            pace = True
            psum += 11
        if dealer1.rank == "Ace" and dealer2.rank == "Ace":
            dsum = 2
        elif dealer1.rank == "Ace" or dealer2.rank == "Ace":
            dace = True
            dsum += 11
        print("\nDealer has a " + str(dealer2.rank) + " of " + dealer2.type + " and another card.\n")
        print("You have a " + str(player1.rank) + " of " + player1.type + " and a " + str(player2.rank) + " of " + player2.type)
        print("\nMoney: " + str(money) + "\nBet: " + str(bet))
        if psum == 21:
            print("Blackjack! You win!")
            money += bet * 2
            continue
        while True:
            bust = False
            print("\nOptions\n1.Hit\n2.Stand\n3.View Cards\n4.Increase Bet\n5.Exit")
            choice = raw_input()

            if choice == "1":
                card = cards.pop()
                out = 0
                cardcounter += 1
                pcards.append(card)
                psum += jqk(card)
                print("\nYou draw a " + str(card.rank) + " of " + card.type)
                if card.rank == "Ace":
                    if psum + 11 > 21:
                        psum += 1
                    else:
                        psum += 11
                        pace = True
                if pace and psum > 21:
                    psum -= 10
                    pace = False
                if psum > 21:
                    print("\nYou bust with " + str(psum) + " against dealers " + str(dsum) + ". Better luck next time.")
                    money -= bet
                    out = 1
                elif psum < 21:
                    print("You now have ")
                    for card in pcards:
                        print(str(card.rank) + " of " + card.type)
                    continue
                else:
                    print("\nBlackjack! You win!")
                    money += bet * 1.5
                    out = 1
                if out == 1:
                    out = 0
                    for card in pcards:
                        cards.insert(0, card)
                    for card in dcards:
                        cards.insert(0, card)
                    break

            elif choice == "2":
                step = False
                print("\nDealer has a " + str(dealer2.rank) + " of " + dealer2.type + " and a " + str(dealer1.rank) + " of " + dealer1.type)
                if dsum > psum:
                    print("\nDealer wins with " + str(dsum) + " against your " + str(psum))
                    money -= bet
                    break
                while dsum < 17:
                    step = True
                    card = cards.pop()
                    cardcounter += 1
                    dsum += jqk(card)
                    dcards.append(card)
                    if card.rank == "Ace":
                        if dsum + 11 <= 21:
                            print("ace less than 21")
                            dsum += 11
                        else:
                            print("ace greater than 21")
                            dsum += 1
                        dace = True
                    #print("\n\ndsum = " + str(dsum) + "\n\n")
                    print("\nDealer drew a " + str(card.rank) + " of " + card.type)
                    print("\nDealer now has \n")
                    for card in dcards:
                        print(str(card.rank) + " of " + card.type)
                    if dsum > 21 and not dace:
                        print("Dealer busts with " + str(dsum) + ". You win!")
                        money += bet * 1.5
                        bust = True
                        break
                    elif dsum > 21 and dace:
                        dsum -= 10
                        dace = False
                    elif dsum <= 21 and dsum > psum:
                        print("\nDealer wins with " + str(dsum) + " against your " + str(psum) + ". Better luck next time.")
                        money -= bet
                        bust = True
                        break
                    elif dsum >17 and dsum == psum:
                        print("\nBoth of you have " + str(dsum) + ". You break even.")
                        bust = True
                        break
                if step == False and dsum < 22 and dsum > 17 and dsum > psum:
                    print("\nDealer wins with " + str(dsum) + " against your " + str(psum) + ". Better luck next time.")
                    money -= bet
                elif dsum < psum:
                    print("\nYou win with " + str(psum) + " against dealer's " + str(dsum))
                    money += bet * 1.5
                elif dsum == psum:
                    print("\nBoth of you have " + str(psum) + ". You break even.")
                for card in pcards:
                    cards.insert(0, card)
                for card in dcards:
                    cards.insert(0, card)
                break
            elif choice == "3":
                print("\nDealer has " + str(dealer2.rank) + " of " + dealer2.type + "\nYou have \n")
                for card in pcards:
                    print(str(card.rank) + " of " + card.type)
            elif choice == "4":
                newbet = 0
                while True:
                    newbet = raw_input("Please enter your new bet\n")
                    if float(newbet) > money:
                        print("You don't have that much money!\n")
                    else:
                        bet = float(newbet)
                        break
            elif choice == "5":
                exit()
            else:
                print("Try again")
        User = raw_input("Continue?")
        if User != "1":
            break
        else:
            continue





    return






while True:
    user = raw_input("Please select a choice: \n1.Play Game\n2.Watch AI\n")
    if user == "1":
        game()
    elif user == "2":
        r = Robot()
        roboGame(r)

    else:
        print("That's not a choice!")
