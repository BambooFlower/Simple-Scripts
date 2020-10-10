import os
import time
import requests
import threading

class Game():
    def __init__(self):
        self.stop = False
        
        self.pot_size = -1
        self.turn_id = -1
        self.who_won = None
        self.match_end = False

        # 0 - no cards, 1 - flop, 2 - street, 3 - river
        self.card_reveal_stage = 0
        
        self.cards_on_table = []
        self.player_tmp = {'self':False,
              'active':False,
              'name':'',
              'folded':False,
              'raised-hist':[],
              'chips':-1,
              'checked':False,
              'called':False,
              'all-in':-1,
              'xp':-1,
              'empty-sit':True,
              'active-turn':False,
              'big-blind':None,
              'small-blind':None,
              'sel-option':None
                           }
        self.final_cards = []
        self.players = {0:dict(self.player_tmp),
            1:dict(self.player_tmp),
            2:dict(self.player_tmp),
            3:dict(self.player_tmp),
            4:dict(self.player_tmp)
        }

    def reset_players(self):
        for i in range(5):
            self.players[i]['checked'] = False
            self.players[i]['called'] = False
            self.players[i]['all-in'] = -1
            self.players[i]['folded'] = False
            self.players[i]['small-blind'] = None
            self.players[i]['big-blind'] = None
            self.players[i]['active-turn'] = False
            self.players[i]['sel-option'] = None
        self.pot_size = 0

    def get_chips(self):
        for i in range(5):
            print(G.players[i]['chips'],i,G.players[i]['empty-sit'])

    def get_checked(self):
        for i in range(5):
            print(G.players[i]['active-turn'],i,G.players[i]['empty-sit'],G.players[i]['chips'])

    def clear_mitm_flow(self):
        r1 = requests.get("http://127.0.0.1:8080/")
        jar = r1.cookies
        csrf_token = jar.get('_xsrf')
        r2 = requests.post("http://127.0.0.1:8080/clear?_xsrf={0}".format(csrf_token), cookies=jar)

    def read_file(self):
        while not self.stop: 
            if not os.path.exists('wss.out'):
                continue
            with open('wss.out','r') as f:
                read_val = [line.split() for line in f]
            
            for l in read_val:
                # Find cards on table
        #        if "Pot" in l[2] or "flop" in l[2] or "pot" in l[2]:
        #            print(l[2:])
                
                # Money in the pot
                #if "rakedPot" in l[2]:
                #    print('\n\nPot won',l[2])
                if "makePot" in l[2]:
                    tmp = l[2].replace("%xt%makePot%-1%",'').replace("'",'').split("%")
                    n_players = int(tmp[0])
                    self.pot_size = 0
                    for i in range(n_players):
                        self.pot_size += int(tmp[i+1])
                    #print(tmp,self.pot_size)
                    #self.players['pot'] = int(self.pot_size)
                    #print('Pot size',self.pot_size)
                    #print(l[2])

                    for i in range(5):
                        if self.players[i]['sel-option'] != 'folded':
                            self.players[i]['sel-option'] = None
                elif "flop" in l[2]:
                    #   print('initial cards',l[2])
                    # 0 rhombus
                    # 1 hearts
                    # 2 shovel
                    # 3 cross

                    # 2 3 4 5 6 7 8 9 10 J  K  Q  A
                    # 2 3 4 5 6 7 8 9 10 11 12 13 14

                    tmp = l[2].replace('%xt%flop%-1%','').replace("'",'').split('%')
                    poses = [2*i for i in range(3)]
                    for i in poses:
                        self.cards_on_table.append({'value':eval(tmp[i]),'suit':eval(tmp[i+1])})
                        pass
                    #print(cards_on_table)
                    self.card_reveal_stage = 1
                    pass
                elif 'heartBeat' in l[2] or 'heartbear' in l[2]:
                    pass
                elif "rakedPot" in l[2]:
                    # Won size
                    #print(l[2])
                    pass
                elif "street" in l[2][:20]:
                    #print('street card',l[2])
                    tmp = l[2].replace('%xt%street%-1%','').replace("'",'').split('%')
                    self.cards_on_table.append({'value':eval(tmp[0]),'suit':eval(tmp[1])})
                    #print(cards_on_table)
                    self.card_reveal_stage = 2
                    pass
                elif "river" in l[2]:
                    #print('river card',l[2])
                    tmp = l[2].replace('%xt%river%-1%','').replace("'",'').split('%')
                    self.cards_on_table.append({'value':eval(tmp[0]),'suit':eval(tmp[1])})
                    #print(cards_on_table)
                    self.card_reveal_stage = 3
                    pass
                elif "winners" in l[2]:
                    # sno is the winner id
                    tmp = l[2].replace('%xt%winnersV2%-1%','').replace("'",'')
                    tmp += '"}]}'
                    tmp = eval(tmp)
                    p_id = tmp['ws'][0]['sno']
                    self.players[p_id]['chips'] = tmp['ws'][0]['ch']
                    self.who_won = int(p_id)
                    self.match_end = True
                    #print('player {} won {}'.format(p_id,tmp['ws'][0]['ch']))
                    #print("---")

                    self.reset_players()
                    #print(tmp)
                    pass
                elif "winner" in l[2]:
                    print(l[2])
                    pass
                elif 'markTurn' in l[2]:
                    turn_id = eval(l[2].replace('%xt%markTurn%-1%','').replace('%0%10%',''))
                    for i in range(5):
                        if i == int(turn_id):
                            self.players[i]['active-turn']  = True
                        else:
                            self.players[i]['active-turn']  = False
                    #print(players[int(turn_id)])
                    
                elif 'xt%raise%' in l[2]:
                    tmp = l[2].replace('%xt%raise%-1%','').replace("'",'').split('%')
                    #print('raise',tmp)
                    p_id =int(eval(tmp[0]))
                    tt = self.players[p_id]['raised-hist'][:]
                    tt.append(eval(tmp[1]))
                    self.players[p_id]['raised-hist'] = tt
                    self.players[p_id]['chips'] = eval(tmp[2])
                    self.players[p_id]['sel-option'] = 'raised'
                    #print('player {} raised {} they now have {} left'.format(tmp[0],tmp[1],tmp[2]))
                elif '%xt%callOption%-1%' in l[2]:
                    # User call option
                    pass
                elif 'call' in l[2][:20]:
                    #print(l[2])
                    tmp = l[2].replace("%xt%call%-1%",'').replace("'",'').split('%')
                    p_id = int(eval(tmp[0]))
                    if tmp[1] == '0':
                        #print('checked',tmp)
                        #print('player {} checked'.format(p_id))
                        self.players[p_id]['sel-option'] = 'checked'
                        self.players[p_id]['chips'] = eval(tmp[2])
                        pass
                    else:
                        #print('player {} called {}'.format(tmp[0],tmp[1]))
                        #print('called',tmp)
                        self.players[p_id]['sel-option'] = 'called'
                        self.players[p_id]['chips'] = eval(tmp[2])
                        pass
                elif 'allin%' in l[2]:
                    tmp = l[2].replace('%xt%allin%-1%','').replace("'",'').split('%')
                    #print('allin',tmp)
                    p_id = int(eval(tmp[0]))
                    self.players[p_id]['all-in'] = tmp[0]
                    self.players[p_id]['chips'] = eval(tmp[2])
                    self.players[p_id]['sel-option'] = 'all-in'
                    #print(who_all_in)
                    #print("player {} all in with {}".format(tmp[0],tmp[1]))
                elif 'allin' in l[2]:
                    # Other player cards
                    tmp = l[2].replace('xt%allinwar%-1%','').replace("'",'')[1:-1]
                    tmp = tmp.split("%")
                    poses = [5*i for i in range(len(tmp)//5)]
                    for i in poses:
                        self.final_cards.append({'sit':tmp[i],
                                                'card1':tmp[i+1],
                                                'suit1':tmp[i+2],

                                                'card2':tmp[i+3],
                                                'suit2':tmp[i+4]
                                            }

                                           )
                        #print(final_cards)
                    pass
                elif 'blindPosted' in l[2]:
                    tmp = eval(l[2].replace('%xt%blindPosted%-1%','').replace("'",'').replace('%',''))
                    #print(tmp)
                    if tmp['t'] == 'sb':
                        self.players[tmp['s']]['small-blind'] = tmp['b']
                        self.players[tmp['s']]['chips'] = tmp['c']
                    elif tmp['t'] == 'bb':
                        self.players[tmp['s']]['big-blind'] = tmp['b']
                        self.players[tmp['s']]['chips'] = tmp['c']
                    #print(tmp)
                    #print(l[2].split("%"))
                    pass
                elif 'fold' in l[2][:40]:
                    who_folded = eval(l[2][len('%xt%fold%-1%')+1])
                    self.players[who_folded]['sel-option'] = 'folded'
                    self.players[who_folded]['folded'] = True
                    #print(who_folded,'folded')
                elif 'clear' in l[2]:
                    #print('New Game')
                    #reset_players()
                    self.match_end = False
                    for i in range(5):
                        self.players[i]['checked'] = False
                    pass
                elif 'updateChips' in l[2]:
                    tmp = l[2].replace('%xt%updateChips%-1%','').replace("'",'').split('%')
                    poses = [3*i for i in range(len(tmp)//3)]
                    for i in poses:
                        #print('{} has {} chips and {}xp'.format(tmp[i],tmp[i+1],tmp[i+2]))
                        self.players[int(tmp[i])]['active'] = True
                        self.players[int(tmp[i])]['chips'] = int(tmp[i+1])
                        self.players[int(tmp[i])]['xp'] = int(tmp[i+2])
                        #self.players[int(tmp[i])]['sit'] = int(tmp[i])

                    #for i in range(4):
                        #if players[i]['active']:
                            #if players[i]['active']:
                                #print(players[i]['sit'],players[i]['chips'])
                    #print('update chips')
                    pass
                elif 'dealHoles' in l[2]:
                    #print('remove cards')
                    self.cards_on_table = []
                    self.final_cards = []
                    self.card_reveal_stage = 0
                    self.turn_id = -1
                    self.clear_mitm_flow()
                    self.match_end = False
                    self.who_won = None
                    for i in range(5):
                        self.players[i]['checked'] = False
                    #reset_players()
                    #print("---")
                elif 'userLost' in l[2]:
                    tmp = eval(l[2].replace('%xt%userLost%-1%','').replace('%','').replace("'",''))
                    #print(type(tmp))
                    self.players[tmp] = dict(self.player_tmp)
                    self.players[tmp]['empty-sit'] = True
                    #print(tmp,'has left')
                elif 'clientHeartbeat' in l[2]:
                    pass
                elif 'dealerTipped' in l[2]:
                    # Can see who tipped the dealer with how much
                    pass
                elif 'defaultWinner' in l[2]:
                    tmp = l[2].replace('%xt%defaultWinner%-1%','').replace("'",'').split('%')
                    p_id = eval(tmp[0])
                    self.who_won = int(p_id)
                    self.match_end = True
                    #print('player {} won {}'.format(p_id,tmp[1]))
                    #print("---")
                    self.reset_players()
                elif 'turnChanged' in l[2]:
                    # I think this shows which player starts
                    tmp = l[2].replace('%xt%turnChanged%-1%','').replace("'",'').split("%")
                    #print('player {} starts'.format(tmp[0]))
                elif 'leaguesV2UserInfo' in l[2]:
                    # I think this shows where each player is and how many turns they play
                    tmp = eval(eval(l[2].replace('%xt%leaguesV2UserInfo%-1%','').replace('%','')))
                    active_usrs = []
                    for i in range(len(tmp)):
                        self.players[tmp[i]['s']]['empty-sit'] = False
                        active_usrs.append(tmp[i]['s'])
                    #print(active_usrs)
                    for i in range(5):
                        if not i in active_usrs:
                            self.players[i] = dict(self.player_tmp)
                            self.players[i]['chips'] = -1
                        #print(tmp[i]['s'])
                    #print('sits and turn count',tmp)
                    pass
                elif 'sitJoined' in l[2]:
                    tmp = l[2].replace('%xt%sitJoined%-1%','').replace("'",'').split('%')
                    if len(tmp) > 1:
                        #print('{} joined at sit {} they have {}xp and {} chips'.format(tmp[0],tmp[3],tmp[1],tmp[2]))
                        self.players[int(tmp[3])]['active'] = True
                        self.players[int(tmp[3])]['name'] = tmp[0]
                        self.players[int(tmp[3])]['chips'] = tmp[2]
                        self.players[int(tmp[3])]['empty-sit'] = False
                        self.players[int(tmp[3])]['sel-option'] = 'folded'
                    
                    pass
                elif 'specJoined' in l[2]:
                    pass
                elif 'overBet' in l[2]:
                    pass
                else:
                    pass
                    #print(l[2])
            #print(pot_size)
            if round(time.time()) - time.time() < 1:
                #print("-----")
                #print(pot_size)
                for i in range(5):
                    #if players[i]['active']:
                    #print()
                    #print(i,players[i]['chips'])
                    pass
            ##            print(l[2])
                # New game
        #        elif 'Winners' in l[2]:
        #            print("-----")
        #        else:
        #            print(l[2])

            os.remove('wss.out')
            time.sleep(0.2)

#G = Game()
#x = threading.Thread(target=G.read_file)
#x.daemon = True
#x.start()
