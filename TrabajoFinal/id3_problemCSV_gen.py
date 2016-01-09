print 'attr1,attr2,attr3,attr4,class'
for a in range(1,4):
  for b in range(1,4):
    for c in range(1,4):
      for d in range(1,4):
        if (a==1 and b==1) or (c==1 and d==1):
          print 'a'+str(a)+',b'+str(b)+',c'+str(c)+',d'+str(d)+',class_1'
        else:
          print 'a'+str(a)+',b'+str(b)+',c'+str(c)+',d'+str(d)+',class_2'
