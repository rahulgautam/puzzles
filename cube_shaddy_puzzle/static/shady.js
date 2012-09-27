/* 
 * JavaScript for Shadow
 * Team name - CUBE
 * Version - 1.1
 * Date - 7-Sept-2012
 */


var cellWidth=50;
var cellHeight=50;
var startX=50;
var startY=50;
var context=null;
var canvasElement=null;
var cells = null;
var cellArray=null;
var solutionArray=null;
var infoXAxis=null;
var infoYAxis=null;
var randomIndex=null;
var numberOfMmoves=0;
var tempNumberOfMmoves=0;
var numberMovesDiv=null;
var canvasHeading=null;
var stylePaddingLeft = 0, stylePaddingTop=0, styleBorderLeft=0, styleBorderTop=0, htmlTop=0, htmlLeft=0,  html=null;
var solutionArray=null;
var emptyArray=null;
var tournament = 1

var inputMoves = $("#input").find("#message");

var msgForm = $("#messageform");


function getArray(){
        var args = {"_xsrf": getCookie("_xsrf"), "gametype": gametype, "tournament": tournament};
        $.ajax({url: "/game/cube/getarray", type: "POST", dataType: "text", cache: false,
                data: $.param(args), success:function(response){
						response=eval("(" + response + ")");
						if(response.success==0)
						{
							//alert(response.cells);
							cells = response.cells+1;
							cellArray=response.cells_array;
							emptyArray=deepObjCopy(response.cells_array);
							//solutionArray=solutionGrid[randomIndex][2];
							infoXAxis=response.y_axis;
							infoYAxis=response.x_axis;	
							//alert("cells"+cells);
							drawCanvas();
						}
						else
						{
							alert(response.result);
							cells = 0;
							cellArray=[[]];
							//solutionArray=solutionGrid[randomIndex][2];
							infoXAxis=[];
							infoYAxis=[];	
						}
					}
              });
}

function getRandom(){
        var args = {"_xsrf": getCookie("_xsrf"), "gametype": gametype, "tournament": tournament};
        $.ajax({url: "/game/cube/random", type: "POST", dataType: "text", cache: false,
                data: $.param(args), success:function(response){
						response=eval("(" + response + ")");
						if(response.success==0)
						{
							//alert(response.cells);
							cells = response.cells+1;
							cellArray=response.cells_array;
							//solutionArray=solutionGrid[randomIndex][2];
							infoXAxis=response.y_axis;
							infoYAxis=response.x_axis;	
							//alert("cells"+cells);
							drawCanvas();
						}
						else
						{
							alert(response.result);
							cells = 0;
							cellArray=[[]];
							//solutionArray=solutionGrid[randomIndex][2];
							infoXAxis=[];
							infoYAxis=[];	
						}
					}
              });
}


function getSolution(){
		//"user":$("div#nav").attr("name")
        var args = {"_xsrf": getCookie("_xsrf"), "gametype": gametype, "tournament": tournament};
        $.ajax({url: "/game/cube/getsolution", type: "POST", dataType: "text", cache: false,
                data: $.param(args), success:function(response){
						response=eval("(" + response + ")");
						if(response.success==0)
						{
							solutionArray=response.result;
							//alert(response.result);
							showSolution();
						}
						else
						{
							alert(response.result);
						}
					}
              });
}

function checkSolution(){
	if(numberOfMmoves==-1)
	{
		canvasHeading.innerHTML="<pre> Info : I know its my answer :D .</pre>";		
	}
	else
	{
        var args = {"_xsrf": getCookie("_xsrf"), "gametype": gametype, "tournament": tournament, "solution": cellArray.toString()};
        $.ajax({url: "/game/cube/checksolution", type: "POST", dataType: "text", cache: false,
                data: $.param(args), success:function(response){
						response=eval("(" + response + ")");
						if(response.success==0)
						{
							
							//alert(response.result);
							compareSolution(response.result);
						}
						else
						{
							alert(response.result);
						}
					}
              });
     }
}




function shadyInit()
{
	numberOfMmoves=0;
	getArray();
	
}

function drawCanvas() {
	//numberOfMmoves=0;
	
    canvasElement = document.getElementById("canvas_cube");
	canvasHeading=document.getElementById("canvasHeading");
	numberMovesDiv=document.getElementById("number_moves");
	canvasHeading.innerHTML="<pre> Info :"+(cells-1)+"*"+(cells-1)+" grid</pre>";
    context = canvasElement.getContext("2d");
	canvasElement.width=cellWidth*(cells+1);
	canvasElement.height=cellHeight*(cells+1);
	context.font = "bold 13px sans-serif";
	context.textAlign = "center";
	context.textBaseline = "bottom";
	i=0;
	  for (var x = 50.5; x <cellWidth*(cells+1); x += cellWidth) {
		context.moveTo(x, 0);
		context.lineTo(x, cellWidth*(cells));
		if(i<cells-1)
			context.fillText(infoXAxis[i], startX*(i+1)+startX/2, startY);
		i++;
		}
	i=0;
	for (var y = 50.5; y < cellHeight*(cells+1); y += cellHeight) {
		context.moveTo(0, y);
		context.lineTo(cellHeight*(cells), y);
		if(i<cells-1)
			context.fillText(infoYAxis[i], startX/2, startY*(i+1)+startY/2);
		i++;	
	}

	context.strokeStyle = "BLACK";
	context.stroke();
	canvasElement.addEventListener("click", canvasClick, false);
	numberMovesDiv.innerHTML="<pre> Moves : "+numberOfMmoves+"</pre>";
	
	
	stylePaddingLeft = parseInt(document.defaultView.getComputedStyle(canvasElement, null)['paddingLeft'], 10)      || 0;
	stylePaddingTop  = parseInt(document.defaultView.getComputedStyle(canvasElement, null)['paddingTop'], 10)       || 0;
	styleBorderLeft  = parseInt(document.defaultView.getComputedStyle(canvasElement, null)['borderLeftWidth'], 10)  || 0;
	styleBorderTop   = parseInt(document.defaultView.getComputedStyle(canvasElement, null)['borderTopWidth'], 10)   || 0;
	var html = document.body.parentNode;
	htmlTop = html.offsetTop;
	htmlLeft = html.offsetLeft;
}

function canvasClick(e) {
    var x;
    var y;
    if (e.pageX != undefined && e.pageY != undefined) {
		var element = canvasElement, offsetX = 0, offsetY = 0, mx, my;
		if (element.offsetParent !== undefined) {
		do {
		  offsetX += element.offsetLeft;
		  offsetY += element.offsetTop;
		} while ((element = element.offsetParent));
		}

		// Add padding and border style widths to offset
		// Also add the <html> offsets in case there's a position:fixed bar (like the stumbleupon bar)
		// This part is not strictly necessary, it depends on your styling
		offsetX += stylePaddingLeft + styleBorderLeft + htmlLeft;
		offsetY += stylePaddingTop + styleBorderTop + htmlTop;

		x = e.pageX - offsetX;
		y = e.pageY - offsetY;

		// We return a simple javascript object with x and y defined


		if(x<cellWidth*cells)
			i=Math.floor(x/cellWidth);
		if(y<cellHeight*cells)
			j=Math.floor(y/cellHeight);
		//alert(i+","+j);
		if(numberOfMmoves==-1)
			numberMovesDiv.innerHTML="<pre> Moves : You have seen the answer.</pre>";
		else
		if(i>0 && j>0)
		{
			numberOfMmoves++;
			numberMovesDiv.innerHTML="<pre> Moves : "+numberOfMmoves+"</pre>";
    
			if(cellArray[i][j]!='1')
				{
					context.fillRect(i*cellWidth+2,j*cellHeight+2,cellWidth-3,cellHeight-3);
					cellArray[i][j]=1;
				}
			else
				{
					cellArray[i][j]=0;
					context.clearRect(i*cellWidth+2,j*cellHeight+2,cellWidth-3,cellHeight-3);
				}
			
			sendMove(numberOfMmoves);
			//$("#submit_scores").click();
		}	
		
    }
	
   
}

function compareSolution(result)
{
	if(numberOfMmoves==-1)
		canvasHeading.innerHTML="<pre> Info : I know its my answer :D .</pre>";
	else
		if(result=='1'){
		    sendMove(numberOfMmoves+" Correct ")
			canvasHeading.innerHTML="<pre> Info : Correct solution.</pre>";
		}
		else
			canvasHeading.innerHTML="<pre> Info : Incorrect solution.</pre>";
}


function showSolutionLoop(i,j)
{
		if(i<solutionArray.length)
		{
			if(j<solutionArray[i].length)
			{
				if(solutionArray[i][j]=='1')
				{
					context.fillRect(i*cellWidth+2,j*cellHeight+2,cellWidth-3,cellHeight-3);
					
				}
				j++;
				myVar=setTimeout(function(){showSolutionLoop(i,j)},20);
			}
			else
			{
					j=0;
					i++;
					myVar=setTimeout(function(){showSolutionLoop(i,j)},20);
			}
		
		}
		else
		{
			i=0;
			clearInterval(myVar);
		}
}

function deepObjCopy(dupeObj) {
       var retObj = new Object();
       if (typeof(dupeObj) == 'object') {
               if (typeof(dupeObj.length) != 'undefined')
                       var retObj = new Array();
               for (var objInd in dupeObj) {        
                       if (typeof(dupeObj[objInd]) == 'object') {
                               retObj[objInd] = deepObjCopy(dupeObj[objInd]);
                       } else if (typeof(dupeObj[objInd]) == 'string') {
                               retObj[objInd] = dupeObj[objInd];
                       } else if (typeof(dupeObj[objInd]) == 'number') {
                               retObj[objInd] = dupeObj[objInd];
                       } else if (typeof(dupeObj[objInd]) == 'boolean') {
                               ((dupeObj[objInd] == true) ? retObj[objInd] = true : retObj[objInd] = false);
                       }
               }
       }
       return retObj;
}

function sendMove(moves){
            if(gametype=='tournament')
            {			
		        inputMoves.val(moves);
		        msgForm.submit();
		        inputMoves.val('');	
		    }
}
function resetCanvas(){
	if(numberOfMmoves==-1)
		numberOfMmoves=0;
	else
		numberOfMmoves=2*numberOfMmoves;
	cellArray=deepObjCopy(emptyArray);
	drawCanvas();
}

function showSolution()
{
	if(numberOfMmoves==0)
		canvasHeading.innerHTML="<pre> Info : Come on don't be lazy, try atleast once.</pre>";
	else
	{
		if(numberOfMmoves!=-1)
			tempNumberOfMmoves=numberOfMmoves;
		drawCanvas();
		numberOfMmoves=-1;
		numberMovesDiv.innerHTML="<pre> Moves : "+tempNumberOfMmoves+"</pre>";
		sendMove(tempNumberOfMmoves+"(Solution seen)");
		showSolutionLoop(0,0);
		/*for(var i=0;i<solutionArray.length;i++)
			{
			for(var j=0;j<solutionArray[i].length;j++)
			{
				if(solutionArray[i][j]==1)
				{
					setTimeout(function(){context.fillRect(i*cellWidth+2,j*cellHeight+2,cellWidth-3,cellHeight-3);},100);
				}
					
			}
		}*/
		cellArray=solutionArray;
		canvasHeading.innerHTML="<pre> Info : Don't give up so early, Try hard next time. </pre>";
	}
}
function getHelp()
{	
		canvasHeading.innerHTML="<pre> Info : Try to solve the puzzle by Blacking out <br> the given squares such that it satisfies <br/> both horizontal & \
vertical conditions.</pre>";
}
