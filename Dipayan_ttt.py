#writen in python 2.7.13
import pygame
import sys
import random
import copy

Q={((0, 0, 0), (0, 0, 0), (0, 0, 0)): 0}
def display_reset():
      global screen
      screen = pygame.display.set_mode((300,300))
      screen.fill((255,255,255))
      pygame.draw.lines(screen,(0,0,0), False, [(100,0),(100,300),(200,300),(200,-1),(300,-1),(300,100),(-1,100),(-1,200),(300,200)], 1)
      pygame.display.set_caption('mouse 1 first player, mouse 2 2nd player')

def value_reset():
      global mylist;global xy;global turn;global win;global alpha;global gamma;global state_saver;global save;global pl;global step_reward;global times_rot;global previous_state;global draw
      mylist = [[0,0,0],[0,0,0],[0,0,0]]
      xy=[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
      turn=0;win=0;alpha=.2;gamma=0.3;w=[3,4];pl=[600,600];step_reward=0.02;times_rot=None;state_saver=None;previous_state=None;draw=0;

def state_maker(pos):
      dum_list=copy.deepcopy(mylist)
##      print mylist
      if pos:
            dum_list[pos[0]][pos[1]]=-1
      global times_rot
      if times_rot:
            for i in range(times_rot):
                   dum_list=zip(*dum_list[::-1])
      else:
            for i in range(4):
                  if dum_list[2][0] or dum_list[2][1]:
                        times_rot=i;break
                  else:
                        dum_list=zip(*dum_list[::-1])
      dum_list=zip(*zip(*dum_list))
##      print "statemaker","\n",dum_list[0],"\n",dum_list[1],"\n",dum_list[2]
      return dum_list

def decesion(num):
      if sum(mylist[0])==num or sum(mylist[1])==num or sum(mylist[2])==num or (mylist[0][0]+mylist[1][1]+mylist[2][2])==num:
            return True
      if sum(zip(*mylist)[0])==num or sum(zip(*mylist)[1])==num or sum(zip(*mylist)[2])==num or zip(*mylist)[0][2]+zip(*mylist)[1][1]+zip(*mylist)[2][0]==num:
            return True
      
def center_dist(pos):
      return abs(pos[0]-1)+abs(pos[1]-1)

def Q_entrier():
##      print "entering"
      global Q;state_maker(None)
##      print "the one that is entering",tuple(state_maker(None))
      if not Q.has_key(tuple(state_maker(None))):
            Q.update({tuple(state_maker(None)):0})
            
def Q_checker(pos):
      global Q;
      if Q.has_key(tuple(state_maker(pos))):
##            print "value found-----", (tuple(state_action[0]),tuple(state_action[1]+[pos])),Q[(tuple(state_action[0]),tuple(state_action[1]+[pos]))]
            return Q[tuple(state_maker(pos))]
      else:
            return 0
      
def Q_updater(win):
      
      global Q;
      if previous_state:
            Q[tuple(previous_state)]=Q[tuple(previous_state)]+alpha*((gamma*Q_checker(None))+win-Q[tuple(previous_state)])
##            print"updating",previous_state,":",Q[tuple(previous_state)],"this with",tuple(state_maker(None)),":",Q_checker(None)
##      for i in Q:
##            print i,":", Q[i]

value_reset()
training = input('Enter number of training required: ')


display_reset()
while True:
        if not training:
            pygame.display.update()
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                   pygame.quit(); sys.exit();
        if not (win or draw):
             if turn==0:
                   if not training:
                         if pygame.mouse.get_pressed()[0]:
                                 turn=1
                         elif pygame.mouse.get_pressed()[2]:
                                 turn=2
                   else:
                         turn=random.randint(1,2);
             else:
                   if not sum(x.count(0) for x in mylist):
                         print("Draw!");win=0;draw=1;Q_updater(win+step_reward)
                   else:
                         if (training or(pygame.mouse.get_pressed()[0] and mylist[pygame.mouse.get_pos()[1]/100][pygame.mouse.get_pos()[0]/100]==0)) and turn%2:
                               if turn!=1:
                                     previous_state=state_maker(None)                                   
                               if training:
                                     pl=random.choice(xy)
                               else:
                                     pl=list(pygame.mouse.get_pos());
                                     pl.reverse();pl=[pl[0]/100,pl[1]/100]
                                     pygame.draw.circle(screen,(0,0,0),(((pl[1])*100)+50,((pl[0])*100)+50),40,3)
                               mylist[pl[0]][pl[1]]=1
                               if not times_rot:
                                     state_maker(None)
                               xy.remove([(pl[0]),(pl[1])])
                               if decesion(3):
                                     win=-20;print("Human Win!")
                               Q_entrier()
                               Q_updater(win+step_reward)
                               turn+=1;
##                               print "--------------------------------------------"
                         elif (training or pygame.mouse.get_pressed()[0]!=1) and (turn+1)%2:
                               Q_list = [[None,None,None],[None,None,None],[None,None,None]]
                               previous_state=state_maker(None)
##                               print xy
                               for i in xy:
                                   Q_list[i[0]][i[1]]=Q_checker(i)
##                               print "Qlist are","\n",Q_list[0];print Q_list[1];print Q_list[2]
                               rd=[[max(i) for i in Q_list].index(max([max(i) for i in Q_list])),Q_list[[max(i) for i in Q_list].index(max([max(i) for i in Q_list]))].index(max([max(i) for i in Q_list]))]
                               if not training:
                                     pygame.draw.lines(screen, (0,0,0), False,[((rd[1]*100)+5,(rd[0]*100)+5),((rd[1]*100)+50,(rd[0]*100)+50),((rd[1]*100)+5,(rd[0]*100)+95)],3)
                                     pygame.draw.lines(screen, (0,0,0), False,[((rd[1]*100)+95,(rd[0]*100)+95),((rd[1]*100)+50,(rd[0]*100)+50),((rd[1]*100)+95,(rd[0]*100)+5)],3)
                               mylist[rd[0]][rd[1]]=-1
                               if not times_rot:
                                     state_maker(None)
                               turn+=1
##                                     print "the one that is going kjkkg", state_saver
                               xy.remove(rd)
                               if decesion(-3):
                                     win=20;print("Human lost!")
                               Q_entrier()
                               Q_updater(win+step_reward)
##                               print "Qlist are","\n"
##                               for i in Q:
##                                     print i,":", Q[i]
##                               print "--------------------------------------------"
        else:
##            for i in Q:
##                   print i,":", Q[i]
            if not training:
                  pygame.time.delay(2000);
            else:
                  training-=1
            display_reset();value_reset();print "training ",training;print "++++++++++++++++++++++++++++++++++++++++++++++++++"


