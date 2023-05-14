ref ={
'O':10 ,'A+':9, 'A':8, 'B+':7 , 'B':6 , 'C':5,'F':0,
'Ab':0}
#ls = [{'grade_earned':'F' },{'grade_earned':'Ab'},{'grade_earned':'A'}]
def sum(ls):
    s=0;
    for r in range(len(ls)):
        s=s+ls[r]
       
    return s

def sgpa(list):
    m_l=[ ]
    c_e=[ ]
    f=0
   
    for r in range(len(list)):
        if(list[r]['grade_earned'] == 'F' or list[r]['grade_earned'] == 'Ab'):
            f=f+1
        
        
        m_l.append(ref[list[r]['grade_earned']]*float(list[r]['subject_credits']))  
        c_e.append(float(list[r]['subject_credits']))   
    sg=sum(m_l)/sum(c_e)
    
    if f == 0 :        
        return sg
    else:
        return 'SGPA Cant be Foundd'
#print(sgpa(ls)) 
def noofcreds(list):
    f=0
    credits=0
    for r in range(len(list)):
        if(list[r]['grade_earned'] == 'F' or list[r]['grade_earned'] == 'Ab'):
            f=f+1
        else:
            credits=credits+float(list[r]['subject_credits'])
    return credits 
    
    
def nooffail(list):
    f=0
    ab=0
    credits=0
    for r in range(len(list)):
        if(list[r]['grade_earned'] == 'F'):
            f=f+1
        elif(list[r]['grade_earned'] == 'Ab'):
            ab=ab+1 
        else:
            pass
    return f,ab
