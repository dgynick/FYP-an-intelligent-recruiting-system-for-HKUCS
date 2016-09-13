
var attributes=["gender","apply_for","major_ug","norm_gpa_ug","norm_gpa_pg","papers","shortlisted","toefl","CET6","onQSRanking","QSRanking"];
var classModel=["decisionTree","logisticRegression"];
var regrModel=["linearRegression","decisionTree"];
var modelType=[classModel,classModel,classModel,regrModel,regrModel,regrModel,classModel,regrModel,regrModel,classModel,regrModel];


var datalist=[];
var sortbyIndex=-1;
var explanation=["M:male F:female",
"apply_for denotes the program the applicant applied for, can be MPhil PhD or Either"
,"undergrad major",
"undergrad gpa(divided by scale)",
"postgrad gpa(divided by scale)",
"#papers published",
"whether the applicant was shortlisted or not",
"toefl score",
"CET6 score: College English test score",
"whether the university the applicant attended as an undergrad is on QSRanking Asia 2016 top100",
"the ranking of the university the applicant attended as an undergrad(if in top100)"];
var onInputList=[];
Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
}
function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}
function viewData(){
    document.getElementById("tab1").class="active";
    document.getElementById("tab2").removeAttribute("class");
    document.getElementById("tab3").removeAttribute("class");
    $("#Modelling").hide();
    $("#StoredResults").hide();
    $("#ViewData").show();
}
function modelling(){
    document.getElementById("tab2").class="active";
    document.getElementById("tab1").removeAttribute("class");
    document.getElementById("tab3").removeAttribute("class");
    $("#ViewData").hide();
    $("#Modelling").show();
    $("#StoredResults").hide();
}

function showStoredResults(){
    document.getElementById("tab3").class="active";
    document.getElementById("tab2").removeAttribute("class");
    document.getElementById("tab1").removeAttribute("class");
    $("#ViewData").hide();
    $("#Modelling").hide();
    $("#StoredResults").show();
}
function loadData(year){
    document.getElementById("data").innerHTML ="<p>fetching data...</p>"
    var indices=[];
    for(var i=0;i<attributes.length;i++){
        indices.push(i);
    }

    $.get("loadData?year="+year,function(data,status){
        var json= JSON.parse(data);
        $.each(json,function(index,value){
            datalist.push(value);
        })
        showData(indices);
    });
}
function showData(indices){
    var table = document.getElementById("data");
    table.innerHTML="";
    var row=table.insertRow(0);
    $.each(indices,function(j,index){
        var cell= row.insertCell(j);
        cell.innerHTML="<a>"+attributes[index]+"</a>";
        cell.onmouseenter= function(){
            $('#explanation').append("<div id='hoveringTooltip' style='position:relative;'></div>");
            $('#hoveringTooltip').html(explanation[index]);
        };
        cell.onmouseleave=function(){
            $('#hoveringTooltip').remove();
        };
        cell.onclick=function(){
            sortbyIndex=index;
            datalist.sort(sortby);
            showData(indices);
        }
    })
    $.each(datalist,function(i,value){
        row=table.insertRow(i+1);
        $.each(indices,function(j,index){
            var cell=row.insertCell(j);
            cell.innerHTML=value[index];
        })
    });

}
function sortby(a,b){
    return (a[sortbyIndex]<b[sortbyIndex]?1:-1);
}
function initializeModellingAttributeList(){
    var table= $("#modellingAttributeList table");
    table.html("");
    var row="<tr>";
    row+="<td>attributes name</td>";
    $.each(attributes,function(index,name){
        row+="<td>"+name+"</td>";
    });
    row +=("</tr>");
    table.append(row);

    row="<tr>";
    row+="<td>select</td>";
    for(var i=0;i<attributes.length;i++){
        row+="<td><input type='checkbox' ID='checkbox"+i+"' checked/></td>";
    }
    row+="</tr>";
    $('#modellingAttributeList table tr:last').after(row);
    $("#modellingAttributeList input").change(function(){
        for(var i=0;i<attributes.length;i++){
            if($("#checkbox"+i).is(":checked")){
                onInputList[i]=true;
            }
            else{
                onInputList[i]=false;
            }
        }
        loadTargetList();
    });
}
function loadTargetList(){
    $("#targets").html("");
    for(var i=0;i<onInputList.length;i++){
        if(onInputList[i]){
            $("#targets").append("<option value='"+i+"'>"+attributes[i]+"</option>");
        }
    }
    loadSampleSize();
    loadModelList();
}
function loadSampleSize(){
    var ivs=[];
    for(var i=0;i<attributes.length;i++){
        if(onInputList[i]&&i!=parseInt($("#targets").val())){
            ivs.push(i);
        }
    }
    $.post("getSampleSize",{iv:ivs,dv:$("#targets").val(),model:$("#models").val()},function(data,status){
        if(parseInt(data)>30){
            $("#sampleSize").html("The current sample size is "+data);
        }
        else{
            $("#sampleSize").html("Warning: The current sample size is too small: "+data+". please consider dropping input such as toefl,gpa_pg and QSRanking");
        }
    });
}
function loadModelList(){
    $("#models").html("");
    $.each(modelType[$("#targets").val()],function(index,value){
        $("#models").append("<option value='"+value+"'>"+value+"</option>");
    });
}
function trainModel(){
    var ivs=[];
    for(var i=0;i<attributes.length;i++){
        if(onInputList[i]&&i!=parseInt($("#targets").val())){
            ivs.push(i);
        }
    }
    if(ivs.contains(10) && ivs.contains(9)){
        alert("can't handle both onQSRanking and QSRanking because onQSRanking is a dummy variable denoting whether QSRanking exists. please drop either");
        return;
    }
    $("#textResult").html("loading...");
    $.post("train",{iv:ivs,dv:$("#targets").val(),model:$("#models").val()},function(data,status){
        json = JSON.parse(data);
        $("#variableExplanation").html("");
        $("#textResult").html("");
        $("#graphResult").html("");
        var vExplain="";
        if(json["ivExplain"]){
            vExplain+=(replaceAll(json["ivExplain"],"\n","<br>"));
        }
        if(json["dvExplain"]){

            vExplain+=(replaceAll(json["dvExplain"],"\n","<br>"));
        }
        $("#variableExplanation").html(vExplain);
        if(json["text"]){
            var text=(replaceAll(json["text"],"\n","<br>"));
            $("#textResult").html(text);
        }
        if(json["graphURL"]){
            var img = document.createElement('img');
            img.src=json["graphURL"];
            $("#graphResult").append(img);
        }
    });
}
$(document).ready(function(){
    $("#tab1").click(function(){
        viewData();
    });
    $("#tab2").click(function(){
        modelling();
    });
    $("#tab3").click(function(){
        showStoredResults();
    });
    loadData(2016);
    viewData();
    initializeModellingAttributeList();
    for(var i=0;i<attributes.length;i++){
        onInputList.push(true);
    }
    loadTargetList();
    $("#targets").change(function(){
        loadModelList();
    });
});