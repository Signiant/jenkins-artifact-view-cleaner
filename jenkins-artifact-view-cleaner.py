#!/usr/bin/python
import urllib2, json, argparse, sys, os, shutil

# Build up the Jenkins API URL for the specified job view
def buildViewURL(jenkins_base_url,view_name):
    full_url = jenkins_base_url.rstrip('/') + "/view/" + view_name + "/api/json"

    return full_url

# Get the list of jobs in a view from a Jenkins server
def getJobsFromJenkins(view_url,debug):
    data = ''

    try:
        response = urllib2.urlopen(view_url)
        data = json.loads(response.read())
    except urllib2.URLError as e:
        print "Error!  Unable to open URL %s : %s" % (view_url, e.reason)

    return data

# See if a directory name exists in a Jenkins view
def findDirInViewList(dir,viewname,viewlist,debug):
    found = False
    # Assume the job name prefix is everything before -branches
    job_name_prefix = viewname.split("-branches")[0]
    job_view_name = job_name_prefix + "-" + dir
    if debug: print "job view name is %s" % job_view_name

    for jobview in viewlist['views']:
        if debug: print "Comparing job view %s to disk name %s" % (jobview['name'],job_view_name)

        if jobview['name'].lower() == job_view_name.lower():
            if debug: print "** Found a match"
            found = True
            break

    return found

def main(argv):
    jenkins_url = ''
    view_name = ''

    parser = argparse.ArgumentParser(description='Clean up a Jenkins artifactor folder.')
    parser.add_argument('-d','--debug', help='Enable more debugging',action='store_true')
    parser.add_argument('-f','--folder', help='Full path to artifacts base folder',required=True)
    parser.add_argument('-j','--jenkinsurl', help='Jenkins Base URL',required=True)
    parser.add_argument('-v','--view',help='Jenkins Branch View Name', required=True)
    parser.add_argument('-r','--dryrun', help='Do not actually delete',action='store_true')

    args = parser.parse_args()

    print 'Jenkins URL=', args.jenkinsurl
    print 'Branch View Name=', args.view
    print 'Artifacts folder=', args.folder
    print 'debug=', args.debug
    print 'dry run=', args.dryrun

    # Build full view URL
    view_url = buildViewURL(args.jenkinsurl,args.view)
    if args.debug: print "view url is ", view_url

    if view_url:
        view_list = getJobsFromJenkins(view_url,args.debug)

        if view_list:
            if args.debug: print "view list ", view_list

            # now loop over all of the folders and see if we have a view
            if os.path.isdir(args.folder):
                subdirectories = os.listdir(args.folder)
                for dir in subdirectories:
                    print "Checking if %s exists in the Jenkins view" % dir

                    if findDirInViewList(dir,args.view,view_list,args.debug):
                        print "branch %s on disk exists in Jenkins - KEEPING" % dir
                    else:
                        # No match - delete from disk
                        print "branch %s exists on disk but not in Jenkins - DELETING" % dir
                        if args.dryrun:
                            print "***** DRY RUN MODE - will not delete %s *****" % dir
                        else:
                            full_branch_path = args.folder.rstrip('/') + "/" + dir
                            if args.debug: print "Full branch path: %s" % full_branch_path

                            if os.path.isdir(full_branch_path):
                                try:
                                    shutil.rmtree(full_branch_path)
                                except Exception,e:
                                    print "ERROR!  Unable to remove %s: %s" % (full_branch_path,str(e))
                            else:
                                print "ERROR!  %s is not a valid directory" % full_branch_path
            else:
                print "ERROR!  %s is not a valid directory" % args.folder
                sys.exit(2)
        else:
            print "ERROR! No jobs found for view ", args.view
            sys.exit(1)

        sys.exit(0)
if __name__ == "__main__":
   main(sys.argv[1:])
