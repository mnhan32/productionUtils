def getJobDependency( root, jobDict, level=0, rootId=0, rootParent=None, dependency=None):
    inputs = root.inputs()
    if inputs:
        level += 1
    for i in inputs:    
        if not i.isBypassed():        
            if level == 1:
                dependency = None
                rootParent = None
                rootId += 1 
                    
            if i.type().name() != 'merge':                
                if i.path() not in jobDict:
                    jobDict['%s'%i.path()] = {}
                    jobDict['%s'%i.path()]['level'] = level
                    jobDict['%s'%i.path()]['id'] = len(jobDict)
                    jobDict['%s'%i.path()]['dependency'] = dependency
                    jobDict['%s'%i.path()]['rootParent'] = rootParent
                    jobDict['%s'%i.path()]['rootId'] = rootId
                    if dependency:
                        jobDict['%s'%i.path()]['dependencyId'] = jobDict[dependency]['id']
                    else:
                        jobDict['%s'%i.path()]['WaitForJobID'] = None
                        
                dependency = i.path()
                
            else:
                if level == 1:
                    rootParent = i.path() 
                dependency = getJobDependency( i, jobDict, level, rootId=rootId, rootParent=rootParent, dependency=dependency)      
            
    return dependency
    

jobDependency = {}
getJobDependency(hou.pwd(), jobDependency )
sorted_jobs = [ {i:jobDependency[i]} for i in sorted(jobDependency, key=lambda x:(jobDependency[x]['rootId'], jobDependency[x]['id']))]
import pprint
pprint.pprint( sorted_jobs )
