#!/usr/bin/env bash

vagrant_box='/home/software/centos7_VirtualBoxVMs5.0.box'
prefix_name='x100speed_transcode'
create_date=`date +%Y%m%d-%H%M%S`
ci_system_name=${prefix_name}'_'${create_date}

box_list=`vagrant box list |grep x100speed_transcode`
if [ -z "$box_list" ]; then
    vagrant box add $ci_system_name $vagrant_box
fi

#create ci system
mkdir -p $ci_system_name
cp x100speed_transcode_ci.sh $ci_system_name
cd $ci_system_name

vagrant init $ci_system_name

sed -i 's/^  # config.vm.network "forwarded_port".*/  config\.vm\.network "forwarded_port", guest: 80, host: 80/g' Vagrantfile
sed -i 's/^  # config\.vm\.provision.*/  config\.vm\.provision "shell", path: "x100speed_transcode_ci.sh"/g' Vagrantfile

vagrant up
