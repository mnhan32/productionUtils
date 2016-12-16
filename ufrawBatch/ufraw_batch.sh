#!/bin/bash

#get bash file location
sPath=$(readlink -f $0)
sBase=$(dirname "${sPath}")
#echo ${sBase}

#add more if needed
supportRaw=(NEF CR2 R3D ORF RW2 DNG ARI TIF)

#date time
dt=$(date '+%d-%m-%Y_%H:%M:%S')
#echo "${sBase}/${dt}.log"



#dialog exist?
useDiaglog=0
if type dialog >> /dev/null 2>&1;then
	useDialog=1
fi 
#echo ${useDialog}

#
if ! type ufraw-batch >> /dev/null 2>&1;then
    echo "This script utilizes ufraw-batch command, can't fine ufraw-batch in your system."
	exit 1
fi
clear
echo "-------------------------------------------------"
echo "-------------- UFraw Batch Convert --------------"
echo "-------------------------------------------------"

#mode sel
opModeArray=(Basic Intermedia Expert)	
echo ""
echo "-------------------------------------------------"
echo "Operation Mode:"
echo "0 ) Basic"
echo "1 ) Intermedia"
echo "2 ) Expert(You will have to define all extra arguments you need)"
read -e -p "choose [0-2]:" -i 0 opMode;
echo ""
echo "#: UFRaw Batch Covert in Mode : ${opModeArray[${opMode}]} "
echo "-------------------------------------------------"

#get source folder
echo ""
echo "-------------------------------------------------"
echo "Select Source Folder"

while [[ ! -d "${sourceF}" ]]
do
	read -e -p "path:" -i "${sBase}" sourceF;
    sourceF=$(readlink -e ${sourceF})
	if [ ! -d "${sourceF}" ];then
		echo "#: Source Folder not exists, re-enter."
	fi
done

echo ""
echo "#: Source Folder is set to ${sourceF}"
echo "-------------------------------------------------"

#Intermeida only
if [ "${opMode}" -ge 1 ];then

#ext filter

#get all existed ext in source folder
allExt=($(find "${sourceF}" -type f -name '*.*' | sed 's@.*/.*\.@@' | sort | uniq))
echo ""
echo "-------------------------------------------------"
echo "Source File Ext Filters"
while true
do
	read -p "Filters:(ALL/NEF/CR2/....,Default=ALL):" sFilter;
	if [ -z ${sFilter} ];then
		if [ -z ${sExt} ];then
			#echo "using default extension: CR2"
			#echo "${sFilter}"
			sExt=${supportRaw[@]}
		fi
		break;
	elif [ "${sFilter}" = "ALL" ];then
		sExt=${supportRaw[@]}
		break;	
	else
		mat=0
		for e in ${allExt[@]}
		do
			if [ "${e^^}" = "${sFilter^^}" ];then
				echo "#: ${sFilter} format added";
				sExt+=(${e});
				mat=1
				break;
			fi
		done
		if [ ${mat} = 0 ];then
			echo "#: Source folder doesn't contain ${sFilter} files."
		fi
	fi
done
echo ""
echo "#: source file extension ${sExt[@]}"
echo "-------------------------------------------------"

fi



if [ ${opMode} -eq 1 ];then
echo ""
echo "-------------------------------------------------"
echo "Save File To"
#target folder
while [[ ! -d "${targetF}" ]]
do 
	read -e -p "Convert File To(Default=Source):" -i "${sourceF}" targetF;
    targetF=$(readlink -e ${targetF})
	if [ ! -d "${targetF}" ];then
		echo "${targetF} no exists."
	fi
done
echo ""
echo "#: Save File to : ${targetF}"
echo ""
#conf file

echo "-------------------------------------------------"
echo "UFaw Id File"
read -e -p "Use UFRaw conf file?(Y/N):" -i "Y" ufrawUse;
if [ "${ufrawUse,,}" = 'y' ];then
	ufrawPreset=($(ls "${sBase}"/*.ufraw))
	idx=0

	if [ ! -z "${ufrawPreset}" ];then
		for e in ${ufrawPreset[@]}
		do
			echo "${idx} ) ${e}"
			((idx++))
		done
	
	fi
	
	if [ ${idx} -eq 0 ];then
		echo "...... no preset found"
	else
		echo "${idx} ) custom path"
	fi


if [ "${idx}" -gt 0 ];then
	read -e -p "choose [0-${idx}]" -i 0 ufrawIdx;
else
	ufrawIdx=${idx}
fi

if [ "${ufrawIdx}" -eq "${idx}" ];then
	while [[ ! -e "${ufrawP}" ]]
		do
            echo "-------------------------------------------------"
			read -e -p "custom preset path:" ufrawP;
			if [ -z "${ufrawP}" ];then
				ufrawUse="N"
				break;
			fi
		done
else
	ufrawP=${ufrawPreset[${ufrawIdx}]}
fi

    echo ""
	echo "#: preset use : ${ufrawP}"
    echo "-------------------------------------------------"
    echo ""
else
    echo ""
	echo "#: no conf used."
    echo "-------------------------------------------------"
fi
else
    targetF="${sourceF}"
    ufrawP="${sBase}/0.default.ufraw"
    sExt=(NEF CR2 R3D ORF RW2)
    outDepth=16
fi

if [ ${opMode} -le 1 ];then
echo "-------------------------------------------------"
echo "OUTPUT FORMAT"
outTypeArray=(ppm tiff tif png jpeg jpg fits)
echo "support format:"
idx=0
for e in ${outTypeArray[@]}
do
	echo "${idx} ) ${e}"
	((idx++))
done


read -e -p "choose one[0-$((idx-1))]" -i 3 outTypeIdx
outType=${outTypeArray[${outTypeIdx}]}
echo ""
echo "#: output as ${outType}"
echo "-------------------------------------------------"
#echo ${outTypeIdx}
if [ ${outTypeIdx} = 4 ] || [ ${outTypeIdx} = 5 ];then
    outDepth=8
fi
fi


if [ "${opMode}" -eq 1 ];then
if [ "${outTypeIdx}" != 4 ] && [ "${outTypeIdx}" != 5 ];then
outDepthArray=(8 16)
echo "-------------------------------------------------"
echo "OUTPUT DEPTH"
echo "support dpeth:"
idx=0
for e in ${outDepthArray[@]}
do
	echo "${idx} ) ${e}"
	((idx++))
done


read -e -p "choose one[0-$((idx-1))]" -i 1 outDepthIdx
outDepth=${outDepthArray[${outDepthIdx}]}
echo ""
echo "#: output as ${outDepth} bit"
echo "-------------------------------------------------"
fi
fi



if [ ${opMode} -ge 1 ];then
echo "-------------------------------------------------"
read -p "extra options:" extraOption;
if [ ! -z "${extraOption}" ];then
    echo ""
    echo "#: extra option : ${extraOption}"
    echo "-------------------------------------------------"
fi

fi


cpuT=$(nproc)
cpuAmt=$(((cpuT-cpuT%2)/2))
if [ ${cpuAmt} -ge 2 ];then
echo "-------------------------------------------------"
echo "Split into Mulitiple Jobs"
read -e -p "job limits[1-${cpuAmt}]" -i $(((cpuAmt-(cpuAmt%2))/2)) jobAmt

echo ""
echo "#: job limit : ${jobAmt}."
echo "-------------------------------------------------"
else
	jobAmt=1
fi


echo "-------------------------------------------------"

#sourceF, targetF, sExt[], ufrawP,outType,outDepth,extraOption

#get all files 
for f in ${sExt[@]}
do
	fileL+=($(ls "${sourceF}"/*."${f}" 2>/dev/null))
done
#echo ${fileL[@]}
if [ ${#fileL[@]} -lt 1 ];then
    echo "no files found. exit."
    exit 1
fi


#if file amount less then job amount, 
#job amount eq to file amount
if [ ${jobAmt} -ge ${#fileL[@]} ];then
	jobAmt=${#fileL[@]}
fi
#echo "${#fileL[@]} ${jobAmt}"

if [ ${opMode} -le 1 ];then
#combine cmd
confCmd=""
if [ -e ${ufrawP} ];then
	confCmd=" --conf=${ufrawP}"
fi

tarCmd=""
if [ ${sourceF} != ${targetF} ];then
	tarCmd=" --out-path==${targetF}"
fi

depthCmd=" --out-depth=${outDepth}"
typeCmd=" --out-type=${outType}"
extraCmd=" --nozip --overwrite --lensfun=none --wb=camera"	
if [ -z "${extraOption}" ];then
baseCmd="/usr/bin/ufraw-batch${confCmd}${tarCmd}${depthCmd}${typeCmd}${extraCmd}"
else
baseCmd="/usr/bin/ufraw-batch${confCmd}${tarCmd}${depthCmd}${typeCmd}${extraCmd} ${extraOption}"
fi

else
baseCmd="/usr/bin/ufraw-batch ${extraOption}"
fi

read -e -p "Read to convert?(Y/N)" -i "Y" goConvert
echo ""

if [ ${jobAmt} -gt 1 ];then

idxF=0
for e in $(seq 1 ${jobAmt})
do
    strCmd="${baseCmd}"
    idx=0
	for f in ${fileL[@]}
	do
		#echo "${idxF}   - ${idx}:${f}"
		modulo=$((${idx} % ${jobAmt}))
		#echo "${modulo}  ${idxF}"
		if [ ${modulo} = ${idxF} ];then
            #echo ${f}
			strCmd="${strCmd} ${f}"
		fi
		((idx++))
	done	
	
	#echo "#### ${idxF} #####"
	#echo "${strCmd} &" >> ${sBase}/ufraw_2.log
	if [ "${goConvert,,}" = "y" ];then
        (${strCmd} >> ${sBase}/${dt}.log 2>&1 &)
    else
        echo "${strCmd} &" >> ${sBase}/ufraw.log
    fi
	((idxF++))
done

else
    echo "here"
    strCmd="${baseCmd} ${fileL[@]}"
    if [ "${goConvert,,}" = "y" ];then
        (${strCmd} >> ${sBase}/${dt}.log 2>&1 &)
    else
        echo "${strCmd} &" >> ${sBase}/ufraw.log
    fi
    #echo ${strCmd}

fi

echo "-----------------------"
echo "${jobAmt} jobs created"
echo "source folder : ${sourceF}"
echo "${#fileL[@]} files to convert"
echo "---------end-----------"
echo ""

