import random

"""
@author: Rahul Gautam
@author: Mahipal Chaudhary
@note: Puzzel > Shaddy Puzzel
"""

class RandomCube(object):
    solution_li=[]
    cell_li=[]
    @staticmethod
    def get_random_list(n, total):
        dividers = sorted(random.sample(xrange(1, total), n - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
    
    @staticmethod
    def get_list(size,max_num,total):
        li = RandomCube.get_random_list(size,total)
        if(max(li)>=max_num):
            return RandomCube.get_list(size,max_num,total)
        else:
            return li
    @staticmethod
    def sum_li(li,first=0,second=0,third=0,fourth=0):
        sum_list=0
        for i in li:
            if isinstance(i,list):
                sum_list+=sum(i)
            else:
                sum_list+=i
        return sum_list+first+second+third+fourth
    
    def get_random_cube(self):
        try:
            cells_array=[]    
            cells=random.randint(5,12)
            sum_cells=random.randint((cells*cells)/3+1,(cells*cells)/2+1)
            x_axis=[]
            info_x_axis=[]
            info_y_axis=[]
            li_random=[]
            s=[]
            cube_dict={}
            try:
                li_random=RandomCube.get_list(cells,cells,sum_cells)
            except Exception,e:
                li_random=RandomCube.get_list(cells,cells/2+2,sum_cells)
        
            start_index=0
            for i in range(cells):
                if(li_random[i]>cells/2):
                    x_axis.append(2)
                else:
                    x_axis.append(random.randint(1,min(cells-li_random[i],li_random[i])))
            
#            print "li_random",li_random
            for i in range(cells):
                info_x_axis.append(RandomCube.get_random_list(x_axis[i], li_random[i]))
                
#            print "cells = ",cells
#            print "sum_cells = ",sum_cells
#            print "x_axis = ",x_axis
#            print "info_x_axis = ",info_x_axis
            print_array=[]
            
            for i in info_x_axis:
                current_axis = i
                p=0
                temp_li=[]
                for j in range(len(current_axis)):
                    k = current_axis[j+1:len(current_axis)]
                    if k==[]:
                        k=[0]
                    if j!=0:
                        p = current_axis[j-1] + p +1
                    #print "first input(is )",p," second is ",9-len(ri)+1 -len(ri)+1 - max(k)+1 - ri[j]
                    try:
                        p2 =random.randint(p,cells-1-len(current_axis)+1 -len(current_axis)+1 - max(k)+1 - current_axis[j]-1 -1 )
                    except:
                        if j==0:
                            p2=0
                        else:
                            p2=p+1
                    if p2>=(cells-current_axis[j]):
                        p2=cells-current_axis[j]
                    #print "prob of ",ri[j]," is ",p2
                    temp_li.append(p2)
                    p=p2
                    #print "prob of ",ri[j]," is ", p
                print_array.append(temp_li)
            #print "\n"
            #print "print_array",print_array
            s=[]
            for k in range(cells):
                s.append(['0' for k in range(cells)])
            #print s
            for i in range(cells):
                ll_temp= info_x_axis[i]
                for j in range(len(ll_temp)):
                    t = ll_temp[j]
                    for kl in range(t):
                        s[i][print_array[i][j]+kl]='1'
            
        #    print "complete_array",s
        #    for i in range(cells):
        #        temp_li=[]
        #        for j in range(cells):
        #            if(s[i][j]=="0"):
        #                pass
            info_y_axis = []
            for i in zip(*s):
                count = 0
                tl = []
                flag = 0
                for j in i:
                    if j == '0' and count != 0:
                        tl.append(count)
                        flag = 0
                        count=0
                    elif j=='1':
                        count += 1
                        flag = 1
                if flag:
                    tl.append(count)
                info_y_axis.append(tl)
            #print info_x_axis
            #print info_y_axis
            for i in range(cells+1):
				cells_array.append(['0' for j in range(cells+1)])
            
            s.insert(0, [ '0' for i in range(cells)])
            for i in range(len(s)):
				s[i].insert(0,'0')
            cube_dict["cells_array"]=cells_array
            #print "info_y_axis ",info_y_axis
            cube_dict["cells"]=cells
            cube_dict["y_axis"]=info_x_axis
            cube_dict["x_axis"]=info_y_axis
            cube_dict["sum_cells"]=sum_cells
            cube_dict["solution"]=s
            cube_dict["success"]=0
            return cube_dict
#            print "sum_cells = ",sum_cells
#            print "x_axis = ",x_axis
#            print "info_x_axis = ",info_x_axis
            
                        
        except Exception,e:
            import traceback
            print("Exception in Shaddy Puzzel %s " % traceback.format_exc())
            
            cube_dict["cells"]=cells
            cube_dict["y_axis"]=info_y_axis
            cube_dict["x_axis"]=info_x_axis
            cube_dict["sum_cells"]=sum_cells
            cube_dict["solution"]=s
            cube_dict["success"]=1
            cube_dict["exception"]=traceback.format_exc()
            cube_dict["cells_array"]=cells_array
            return cube_dict
            
#rc = RandomCube()
#cube_dict = rc.get_random_cube()
#if cube_dict['success']==0:
#    for k, v in cube_dict.iteritems():
#        print k," = ", v
