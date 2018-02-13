import os
import subprocess
import pwd
import grp
import shutil

# UID and GID
uid = pwd.getpwnam("root").pw_uid
gid = grp.getgrnam("root").gr_gid

# Create User List
userList = []
userUID = []
userGID = []

# Loop the amount of Jailed Users you want
for i in range(41):
	userList.append("user00" + str(i))

for j in range(0, len(userList)):
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j]])
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j] + "/dev"])
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j] + "/bin"])
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j] + "/lib/x86_64-linux-gnu"])
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j] + "/lib64/ld-linux-x86-64.so.2"])
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j] + "/etc/"])
	subprocess.Popen(["mkdir", "-p", "/home/" + userList[j] + "/home/" + userList[j]])

for k in range(0, len(userList)):
	userUID = pwd.getpwnam(userList[i]).pw_uid
	userGID = grp.getgrnam(userList[i]).gr_gid
	os.chown("/home/" + userList[k], uid, gid)
	os.chmod("/home/" + userList[k], 755)
	os.chown("/home/" + userList[k] + "/home/", userUID, userGID)
	os.chown("/home/" + userList[k] + "/home/" + userList[j], userUID, userGID)
	os.chmod("/home/" + userList[j] + "/home", 700)
	os.chmod("/home/" + userList[j] + "/home/" + userList[j], 700)
	os.chdir("/home/" + userList[k] + "/dev")
	subprocess.Popen(["mknod", "-m", "666", "null", "c", "1", "3"])
	subprocess.Popen(["mknod", "-m", "666", "tty", "c", "5", "0"])
	subprocess.Popen(["mknod", "-m", "666", "zero", "c", "1", "5"])
	subprocess.Popen(["mknod", "-m", "666", "random", "c", "1", "8"])
	os.chdir("/home/" + userList[k] + "/bin")
	shutil.copy2("/bin/bash", "/home/" + userList[k] + "/bin/")
	shutil.copy2("/bin/ls", "/home/" + userList[k] + "/bin/")
	shutil.copy2("/bin/date", "/home/" + userList[k] + "/bin/")
	shutil.copy2("/bin/mkdir", "/home/" + userList[k] + "/bin/")
	shutil.copy2("/lib/x86_64-linux-gnu/libtinfo.so.5", "/home/" + userList[k] + "/lib/x86_64-linux-gnu")
	shutil.copy2("/lib/x86_64-linux-gnu/libdl.so.2", "/home/" + userList[k] + "/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libc.so.6", "/home/" + userList[k] + "/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib64/ld-linux-x86-64.so.2", "/home/" + userList[k] + "/lib64/")
	shutil.copy2("/lib/x86_64-linux-gnu/libselinux.so.1", "/home/" + userList[k] + "/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libpcre.so.3", "/home/" + userList[k] + "/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libpthread.so.0", "/home/" + userList[k] + "/lib/x86_64-linux-gnu/")
	shutil.copy2("/etc/{passwd,group}", "/home/" + userList[k] + "/etc/")
	with open("/etc/ssh/sshd_config", "a") as myfile:
		if(k > 0):
			myfile.write("Match User " + userList[k])
		else:
			myfile.write("#Define Usernames to add to Chroot Jails")
			myfile.write("Match User " + userList[k])

for l in range(0, len(userList)):
	with open("/etc/ssh/sshd_config", "a") as addChrootDir:
		if(l > 0):
			addChrootDir.write("ChrootDirectory /home/" + userList[l])
		else:
			addChrootDir.write("#Specify Chroot Jail Locations")
			addChrootDir.write("ChrootDirectory /home/" + userList[l])


