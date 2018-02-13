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
	userList.append("user" + str(i))
	os.system("sudo useradd " + userList[i])

for j in range(0, len(userList)):
	subprocess.Popen(["mkdir", "-p", "/home/jail"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/dev"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/bin"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/lib/x86_64-linux-gnu"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/lib64"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/etc/"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/usr/lib/x86_64-linux-gnu/"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/usr/bin/"])
	subprocess.Popen(["mkdir", "-p", "/home/jail/home/" + userList[j]])

for k in range(0, len(userList)):
	userUID = pwd.getpwnam(userList[k]).pw_uid
	userGID = grp.getgrnam(userList[k]).gr_gid
	os.chown("/home/jail", uid, gid)
	os.chmod("/home/jail", 0755)
	os.chown("/home/jail/home/", uid, gid)
	os.chown("/home/jail/home/" + userList[k], userUID, userGID)
	os.chmod("/home/jail/home/" + userList[k], 0700)
	os.chdir("/home/jail/dev")
	subprocess.Popen(["mknod", "-m", "666", "null", "c", "1", "3"])
	subprocess.Popen(["mknod", "-m", "666", "tty", "c", "5", "0"])
	subprocess.Popen(["mknod", "-m", "666", "zero", "c", "1", "5"])
	subprocess.Popen(["mknod", "-m", "666", "random", "c", "1", "8"])
	os.chdir("/home/jail/bin")
	shutil.copy2("/bin/sh", "/home/jail/bin/")
	shutil.copy2("/bin/bash", "/home/jail/bin/")
	shutil.copy2("/bin/ls", "/home/jail/bin/")
	shutil.copy2("/bin/date", "/home/jail/bin/")
	shutil.copy2("/bin/mkdir", "/home/jail/bin/")
	shutil.copy2("/bin/nano", "/home/jail/bin/")
	shutil.copy2("/usr/bin/vi", "/home/jail/usr/bin/")
	shutil.copy2("/usr/bin/vim", "/home/jail/usr/bin/")
	shutil.copy2("/lib/x86_64-linux-gnu/libtinfo.so.5", "/home/jail/lib/x86_64-linux-gnu")
	shutil.copy2("/lib/x86_64-linux-gnu/libdl.so.2", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libc.so.6", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib64/ld-linux-x86-64.so.2", "/home/jail/lib64/")
	shutil.copy2("/lib/x86_64-linux-gnu/libselinux.so.1", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libpcre.so.3", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libpthread.so.0", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libm.so.6", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libacl.so.1", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/usr/lib/x86_64-linux-gnu/libgpm.so.2", "/home/jail/usr/lib/x86_64-linux-gnu/")
	shutil.copy2("/usr/lib/x86_64-linux-gnu/libpython3.5m.so.1.0", "/home/jail/usr/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libattr.so.1", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libexpat.so.1", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libz.so.1", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libutil.so.1", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/lib/x86_64-linux-gnu/libncursesw.so.5", "/home/jail/lib/x86_64-linux-gnu/")
	shutil.copy2("/etc/passwd", "/home/jail/etc/")
	shutil.copy2("/etc/group", "/home/jail/etc/")
	with open("/etc/ssh/sshd_config", "a") as myfile:
		if(k > 0):
			myfile.write("Match User " + userList[k] + "\n")
		else:
			myfile.write("#Define Usernames to add to Chroot Jails\n")
			myfile.write("Match User " + userList[k] + "\n")

with open("/etc/ssh/sshd_config", "a") as addChrootDir:
	addChrootDir.write("\n#Specify Chroot Jail Location\n")
	addChrootDir.write("ChrootDirectory /home/jail\n")


