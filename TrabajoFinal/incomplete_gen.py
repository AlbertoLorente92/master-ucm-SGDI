values = [
[1,1,3,3],
[2,1,2,2],
[3,2,1,1],
[4,3,2,2],
[1,2,1,2],
[2,2,2,1],
[3,2,4,1],
[4,4,1,3],
[1,2,3,1],
[2,2,4,2],
[3,2,4,2],
[4,4,3,1],
[1,3,1,3],
[2,3,2,1],
[3,3,1,1],
[5,1,1,2],
[1,3,3,2],
[2,3,3,1],
[3,3,1,2],
[5,1,3,2],
[1,4,1,3],
[2,3,3,3],
[3,3,2,2],
[5,2,2,2],
[1,4,4,1],
[2,4,1,3],
[3,4,2,1],
[5,3,1,2],
[2,1,1,1],
[2,4,2,1],
[4,1,3,2],
[5,3,2,3],
[2,1,1,3],
[3,1,1,1],
[4,1,4,2],
[5,4,1,3],
[2,1,2,1],
[3,1,4,3],
[4,2,1,3],
[5,4,4,3]
]

print 'attr1,attr2,attr3,attr4,class'
for a in range(1,6):
  for b in range(1,5):
    for c in range(1,5):
      for d in range(1,4):
        if not [a,b,c,d] in values:
          continue
        if (a==4 and d==2) or (c==1 and d==1) or (a==2 and c==4 and d==2) or (a==5 and c==4 and d==2):
          print 'a'+str(a)+',b'+str(b)+',c'+str(c)+',d'+str(d)+',class_1'
        else:
          print 'a'+str(a)+',b'+str(b)+',c'+str(c)+',d'+str(d)+',class_2'
