from collections import defaultdict

from utils import pickBest,makeWeightedRule

class GenericApplicant(object):
    def __init__(self,obj=None,attribs=None,attribNames=None):
        if attribs:
            self.attrib = attribs
        else:
            self.attrib = defaultdict(int)
        if attribNames:
            self.attribNames = attribNames
        else:
            self.attribNames = []
        self.obj = obj
        self.options = []
        self.selected = []

class GenericTarget(GenericApplicant):
    def __init__(self,maxSelected=1,obj=None,attribs=None,attribNames=None):
        self.maxApplicants = maxSelected
        super(GenericTarget,self).__init__(obj,attribs,attribNames)
        


class Matchmaker:
    def __init__(self):
        pass
    def match(self,apps,targets):
        """ assumes the applicants and targets implement Applicant and Target """
        self.applicants = apps
        self.targets = targets

        possibleTargets = defaultdict(list)
        for applicant in self.applicants:
            applicant.options = pickBest(self.targets,makeWeightedRule([[applicant.attrib[a],a] for a in applicant.attribNames]),len(self.targets))
            possibleTargets[applicant.options[0]].append(applicant)

        #print "DEBUG"
        #for pt in possibleTargets:
        #    print pt.id,"picked by", str([x.id for x in possibleTargets[pt]])
        #for a in self.applicants:
        #    print a.id,"likes",str([x.id for x in applicant.options])

        rejected = ["bogus"]
        totallyRejected = []

        while rejected:
            rejected = self.filterApplicants(possibleTargets)
            if rejected:
                for app,rejectedJob in rejected:
                    app.options.pop(0)
                    if len(app.options) > 0:
                        possibleTargets[app.options[0]].append(app)
                    else:
                        totallyRejected.append(app)
            #print "DEBUG"
            #for pt in possibleTargets:
            #    print pt.id,"picked by", str([x.id for x in possibleTargets[pt]])
            #for a in self.applicants:
            #    print a.id,"likes",str([x.id for x in a.options])
            #print "Rejected this round was",str([(x.id,y.id) for x,y in rejected])
            #print "Rejected by life was",str([x.id for x in totallyRejected])
                
        for position in possibleTargets:
            position.selected = possibleTargets[position]
            for applicant in position.selected:
                applicant.selected = [position]
        

    def filterApplicants(self,possibleTargets):
        rejectedList = []
        for target in possibleTargets:
            applicants = possibleTargets[target]
            #print "Check, we currently have %d applicants for %d spots" % (len(applicants),target.maxApplicants)
            if len(applicants) > target.maxApplicants:
                possibleTargets[target] = pickBest(applicants,makeWeightedRule([[target.attrib[a],a] for a in target.attribNames]),target.maxApplicants)
                rejectedList += [(app,target) for app in applicants if not app in possibleTargets[target]]
        return rejectedList

                

        
