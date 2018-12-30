import random

projectnos = 4 #binary string size
projectset =10 #population size
levels = 10 #total no. of generations
mutation_chance=0.2
crossover_prob=0.3
weights=[0.2,0.3,0.5,0.1] #weights used in fitness function
c1=[0.5,1.0,1.5,0.1] #constraint 1
c2=[0.3,0.8,1.5,0.4] #constraint 2
c3=[0.2,0.2,0.3,0.1] #constraint 3


def initialiseprojects():
	projectpop=[]
	while len(projectpop)<projectset:
		projval=''
		for proj in range(projectnos):
			projval+=str(random.randint(0,1))
		if projval not in projectpop:
			projectpop.append(projval)

	return projectpop

def list_to_string(projects):
	newprojects=[]
	for j in range(len(projects)):
		final=''
		for i in range(projectnos):
			final+=str(projects[j][i])
		newprojects.append(final)
	return newprojects

def cal_fitness(values):

	value_fitness_list=[]

	finalproj=[]
	for value in values:
		valuestrg=value
		value=list(map(int,value))
		if round(sum(list(map(lambda x,y:x*y,value,c1))),2)<=3.1:
			
			if round(sum(list(map(lambda x,y:x*y,value,c2))),2)<=2.5:
				
				if round(sum(list(map(lambda x,y:x*y,value,c3))),2)<=0.4:
		
					value_fitness_list.append((valuestrg,round(sum(list(map(lambda x,y:x*y,value,weights))),2)))
				else:
					value_fitness_list.append((valuestrg,0))
			else:
				value_fitness_list.append((valuestrg,0))
		else:
			value_fitness_list.append((valuestrg,0))

	print("Population and fitness of each individual:",value_fitness_list)
	indivalfit=[]
	for valfit in value_fitness_list:
		indivalfit.append(valfit[1])
	indivalfit.sort(reverse=True)	
	
	indivalfit.pop()
	fittestgroup=[]
	new_list=[]
	for i in indivalfit:
		if i not in new_list:
			new_list.append(i)

	

	for i in range(len(new_list)):
		for valfit in value_fitness_list: 
			if new_list[i]==valfit[1]:
				fittestgroup.append(valfit[0])

	fittestgroup=list_to_string(fittestgroup)

	return fittestgroup

def check_constraints(projects):

	finalproj=[]
	for value in projects:
		value=list(map(int,value))
		if round(sum(list(map(lambda x,y:x*y,value,c1))),2)<=3.1:

			if round(sum(list(map(lambda x,y:x*y,value,c2))),2)<=2.5:
				
				if round(sum(list(map(lambda x,y:x*y,value,c3))),2)<=0.4:
					
					finalproj.append(value)
	
	newprojects=list_to_string(finalproj)
	
	return newprojects 

def crossover(fitval1,fitval2):

 	prob=random.random()
 	if prob>=crossover_prob:
 		idx=random.randint(1,4)
 		return (fitval1[:idx]+fitval2[idx:], fitval2[:idx]+fitval1[idx:])
 	else:
 		return (fitval1,fitval2)

def cal_fitness_end(value):
	valuestrg=value
	value=list(map(int,value))		
	return (valuestrg,round(sum(list(map(lambda x,y:x*y,value,weights))),2))

def mutation(fitval):

	fitt_val=""
	rand_num=random.random()
	if rand_num < mutation_chance:
	
		rand_number=random.randint(0,projectnos-1)
		for nos in range(0,projectnos):
			if (nos==rand_number):

				if(fitval[rand_number]=='0'):
					fitt_val=fitt_val+'1'
				else:
					fitt_val=fitt_val+'0'
			else:
				fitt_val=fitt_val+str(fitval[nos])	

		return fitt_val
	
	else:
		return fitval

if __name__ == "__main__":

	fittestunit_listlevel=[]
	
	print("Mutation Probability:",mutation_chance)
	print("Population size:",projectset)

	initialprojects = initialiseprojects()
	#print("initial projects",initialprojects)

	for level in range(levels):

		print("GENERATION:",level)	
		#print("initial projects",initialprojects)

		projectparents=cal_fitness(initialprojects)
		print("Individuals selected for cross over:",projectparents)

		offspring_cross=[]
		for i in range(len(projectparents)-1):
			offspring_cross.append(crossover(projectparents[i],projectparents[i+1]))

		offspring_cross_new=[]
		for i in range(len(offspring_cross)):
			for j in range(len(offspring_cross[i])):
				offspring_cross_new.append(offspring_cross[i][j])	
			
		print("Individuals after Cross Over",offspring_cross_new)
			
		offspring_mutate=[]
		for i in range(len(offspring_cross_new)):
			offspring_mutate.append(mutation(offspring_cross_new[i]))

		print("Generated Children:",offspring_mutate)
		parentsretain=[]
		parentsretain=offspring_mutate+projectparents
		print("Children with Parents:",parentsretain)
			
		finalgeneration=check_constraints(parentsretain)
		finalgenerationnew=finalgeneration[:projectset]
		print("final generation",finalgenerationnew)

		fittest_unit = finalgenerationnew[0]
		max_fitness  = cal_fitness_end(finalgenerationnew[0])
		max_fitness  = max_fitness[1]

		for individual in finalgenerationnew:
			ind_fitness = cal_fitness_end(individual)
			ind_fitness = ind_fitness[1]

			if ind_fitness > max_fitness:
				fittest_unit = individual
				max_fitness = ind_fitness

		fittestunit_listlevel.append(fittest_unit)

		initialprojects=finalgenerationnew

		if len(fittestunit_listlevel)>=3:
			for i in range(len(fittestunit_listlevel)-2):
				if  fittestunit_listlevel[i] == fittestunit_listlevel[i+1] and fittestunit_listlevel[i+1] == fittestunit_listlevel[i+2]:
					print("exiting...")
					print("Fittest Binary String:",fittestunit_listlevel[i+2])
					exit(0)
	print("fittest unit after "+level+" generations is :",fittest_unit)				




