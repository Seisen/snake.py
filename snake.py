import pygame
import numpy as np
import random

pygame.init()
clock = pygame.time.Clock()
screen=pygame.display.set_mode((1400,1000))
running=True

font=pygame.font.Font(None, 200)
game_over=font.render("GAME OVER",1,(250,250,250))
font=pygame.font.Font(None, 100)
space=font.render("Press space to restart",1,(250,250,250))
font=pygame.font.Font(None, 50)



mort=False
sens=4

ecran=np.full((140,100),0)
ecran[1][1]=1
agrandir=False
tabCorpx=[]
tabCorpy=[]
mangé=True
liste_couleur=[(250,0,0),(0,250,0),(0,0,250)]


r=0
g=0
b=0



def avance_tete (sens,ecran):
    #1234 bas hautgauche droite
    coo=[]#(x,y)
    trouve=False
    mort=False
     
    for i in range(140):
        for j in range(100):
            if not trouve:
                if ecran[i][j]==1:
                    ecran[i][j]=0
                    if sens==2:
                        ecran[i][j+1]=1
                        coo+=[i*10]
                        coo+=[(j*10)+1]
                        if j+1==97:
                            mort=True
                        trouve=True
                    elif sens==1:
                        ecran[i][j-1]=1
                        coo+=[i*10]
                        coo+=[(j*10)-1]
                        if j-1==1:
                            mort=True
                        trouve=True

                    elif sens==3:
                        ecran[i-1][j]=1
                        coo+=[(i*10)-1]
                        coo+=[j*10]
                        if i-1==1:
                            mort=True
                        trouve=True

                    else:
                        ecran[i+1][j]=1
                        coo+=[(i*10)+1]
                        coo+=[j*10]
                        if i+1==137:
                            mort=True
                        trouve=True

    return coo,mort

def se_touche(tabCorpx,tabCorpy,coo):
    mort=False
    for i in range(2,len(tabCorpx)-1):
        if tabCorpx[i]<coo[0]+2 and tabCorpx[i]>coo[0]-2 and tabCorpy[i]<coo[1]+2 and tabCorpy[i]>coo[1]-2:
            mort=True
    return mort




def corp(tabCorpx,tabCorpy,agrandir,coo):
    tabCorpx[0]=coo[0]
    tabCorpy[0]=coo[1]
    agrax=tabCorpx[len(tabCorpx)-1]
    agray=tabCorpy[len(tabCorpy)-1]
    if agrandir:
        agrandir=False
        tabCorpx+=[agrax]
        tabCorpy+=[agray]
    if len(tabCorpx)>1:
        for i in range(len(tabCorpx)-1,0,-1):
            tabCorpx[i]=tabCorpx[i-1]
            tabCorpy[i]=tabCorpy[i-1]
        
   
    return tabCorpx,tabCorpy,agrandir
cpt=0
def nourriture():
    x=random.randint(1,139)
    y=random.randint(1,99)
    x*=10
    y*=10
    score= font.render(str(),1,(220,250,250))
    return x,y

def get_score(tabCorpx):
    x=len(tabCorpx*5)
    x-=20
    score= font.render("SCORE = "+str(x),1,(220,250,250))
    return score

while running:

    clock.tick(30)
    screen.fill((0,0,0))
    keys = pygame.key.get_pressed()

    score=get_score(tabCorpx)
    if cpt<100:
        cpt+=1
        agrandir=True
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
    if mort:
        screen.blit(game_over,(280,450))
        screen.blit(space,(340,600))
        if keys[pygame.K_SPACE]:
            mort=False
            sens=4
            ecran=np.full((140,100),0)
            ecran[1][1]=1
            agrandir=False
            tabCorpx=[]
            tabCorpy=[]
            mangé=True
            cpt=0


    if keys[pygame.K_z] and sens!=2:
        sens=1
    if keys[pygame.K_s] and sens!=1:
        sens=2
    if keys[pygame.K_q] and sens!=4:
        sens=3
    if keys[pygame.K_d] and sens!=3:
        sens=4

    if not mort:
        if mangé:
            x,y=nourriture()
            couleur=liste_couleur[random.randint(0,2)]
            mangé=False
        
        coo,mort=avance_tete(sens,ecran)
        if len(tabCorpx)==0:
            tabCorpx+=[coo[0]]
            tabCorpy+=[coo[1]]
        tabCorpx,tabCorpy,agrandir=corp(tabCorpx,tabCorpy,agrandir,coo)
        
        for i in range(0,len(coo),2):

            pygame.draw.rect(screen, (250,250,250), (coo[i],coo[i+1],10,10))

        
        for i in range(len(tabCorpx)-1):
            pygame.draw.rect(screen, (250,250,250), (tabCorpx[i],tabCorpy[i],10,10))
        
        if x<coo[0]+2 and x>coo[0]-2 and y<coo[1]+2 and y>coo[1]-2:
            mangé=True
            agrandir=True
        mort=se_touche(tabCorpx,tabCorpy,coo)
        pygame.draw.rect(screen,couleur, (x,y,10,10))

        if coo[0]>1390 or coo[0]<10 or coo[1]>980 or coo[1]<10:
            mort = True
        
        if sens==3 or sens==4:
            pygame.draw.rect(screen, (0,0,0), (coo[0]+1, coo[1]+2,2,2))
            pygame.draw.rect(screen, (0,0,0), (coo[0]+1, coo[1]+7,2,2))
        if sens==1 or sens==2:
            pygame.draw.rect(screen, (0,0,0), (coo[0]+2, coo[1]+1,2,2))
            pygame.draw.rect(screen, (0,0,0), (coo[0]+7, coo[1]+1,2,2))

    if r!=250 and b==0 and g==0:
        r+=10
    elif b!=250 and r!=0 and g==0:
        b+=10
        r-=10
    elif b!=0 and r==0 and g!=250:
        g+=10
        b-=10
    elif g!=0 and b==0:
        g-=10
    arc_en_ciel=[r,g,b]

    pygame.draw.rect(screen,    arc_en_ciel, (0,0,10,1400))
    pygame.draw.rect(screen,    arc_en_ciel, (0,0,1400,10))
    pygame.draw.rect(screen, arc_en_ciel ,(1390,0,10,1400))
    pygame.draw.rect(screen,    arc_en_ciel, (0,990,1400,10))


    screen.blit(score,(1100,20))
    
    pygame.display.flip()
   
   
