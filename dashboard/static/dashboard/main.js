
var user_data;
var flagMenu = false;


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

//send ajax request to django

function oReqListener(){

   console.log(this.response);
    var response = JSON.parse(this.response)
   var activateButton = document.querySelector('#btn'+response.id);
   console.log(activateButton);

   console.log(response);
   if(response.code == 1){

     activateButton.classList.remove('blue');
     activateButton.classList.add('orange');
     activateButton.innerText = 'Deactivate'


   } else if(response.code == 0){
     activateButton.classList.remove('orange');
     activateButton.classList.add('blue');
     activateButton.innerText = 'Activate'
   }
}

function activateProfile(id){

   var oReq = new XMLHttpRequest();
   oReq.addEventListener("load", oReqListener);
   oReq.open("GET", `http://${window.location.hostname}:8000/activate/${id}`);
   oReq.setRequestHeader("X-CSRFToken", csrftoken);
   oReq.send(null);

}

function copy(e){
  navigator.clipboard.writeText(e.innerText).then(
     function(){
        console.log("Async: Copying to clipboard was successful");
     },
     function(err){
        console.log("Async: Could not copy text: ", err);
     }
  )
}
  
function buildMatrix(){
   var response = JSON.parse(this.response);
   console.log(response);
   console.log(user_data);

   config = {
      container:"#matrix",
      animateOnInit: true,
      scrollbar: "fancy",
      levelSeparation:50,
      connectors:{
         type: 'curve'
      },

      animation: {
            nodeAnimation: "easeOutBounce",
            nodeSpeed: 700,
            connectorsAnimation: "bounce",
            connectorsSpeed: 700
        },

      node: {
         HTMLclass: 'ml-child',
         collapsable: true
      }
   };

   if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
      // some code..
      //config.rootOrientation = 'EAST';
   }
    
   let baseUrl = "http://192.168.43.159:8000/static/dashboard/images";
   parent_node = {
      text: {name: response.parent.fname + " " + response.parent.lname},
      image: `${baseUrl}/user.png`,
      
   };

    chart_config = [
      config, parent_node
   ]

   var first_child, second_child, third_child, fourth_child, fifth_child, sixth_child;
   var first_child_data, second_child_data, third_child_data, fourth_child_data, fifth_child_data, sixth_child_data;
   first_child_data = response.children[0];
   second_child_data = response.children[1];


   if(first_child_data){
      first_child = {
         parent: parent_node,
         text: {name: first_child_data.fname + " " + first_child_data.lname},
         image: `${baseUrl}/user.png`

      }
      chart_config.push(first_child)
      third_child_data = first_child_data.children[0];
      fourth_child_data = first_child_data.children[1];
      if(third_child_data){
         third_child = {
             parent: first_child,
             text: {name: third_child_data.fname + " " + third_child_data.lname},
             image: `${baseUrl}/user.png`
         }
         chart_config.push(third_child)
      }

      if(fourth_child_data){
         fourth_child = {
             parent: first_child,
             text: {name: fourth_child_data.fname + " " + fourth_child_data.lname},
             image: `${baseUrl}/user.png`
         }
         chart_config.push(fourth_child)
      }
   }



   if(second_child_data){
     second_child = {
       parent: parent_node,
       text: {name: second_child_data.fname + " " + second_child_data.lname},
       image: `${baseUrl}/user.png`
     }
     chart_config.push(second_child)
     fifth_child_data = second_child_data.children[0]
     sixth_child_data = second_child_data.children[1]

     if(fifth_child_data){
         fifth_child = {
             parent: second_child,
             text: {name: fifth_child_data.fname + " " + fifth_child_data.lname},
             image: `${baseUrl}/user.png`
         }
         chart_config.push(fifth_child)
      }

      if(sixth_child_data){
         sixth_child = {
             parent: second_child,
             text: {name: sixth_child_data.fname + " " + sixth_child_data.lname},
             image: `${baseUrl}/user.png`
         }
         chart_config.push(sixth_child)
      }
   }





   tree = new Treant(chart_config);
}

function getChildren(id){
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load",buildMatrix);
    oReq.open("GET", `http://${window.location.hostname}:8000/fetch/${id}`);
    oReq.send(null);
}



function drawGraph(){

  var canvas = document.getElementById("graph")
  var ctx = canvas.getContext('2d');
  var radius = canvas.height / 2;
  ctx.translate(radius, radius);
  radius = radius * 0.90
  ctx.arc(0,0,radius, 0, 2*Math.PI);
  ctx.fillStyle = "black";
  ctx.fill();

  drawPieSlice(ctx,0,0, radius, Math.PI/2, Math.PI/2 + Math.PI/4, 'red' )

}


window.addEventListener("resize", function(event){
   var menu = document.querySelector('.menu')
   console.log(event);
   if(menu !==null){
      if(event.target.screen.width > 900){
           flagMenu = true;
           menu.style.display = "block";
      }
      

     
     
   }
})

   //myPieChart.draw();
   





function drawLine(ctx, startX, startY, endX, endY){
   ctx.beginPath();
   ctx.moveTo(startX, startY);
   ctx.lineTo(endX, endY);
   ctx.stroke();
}

function drawArc(ctx, centerX, centerY, radius, startAngle, endAngle){
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.stroke();
}

function drawPieSlice(ctx, centerX, centerY, radius, startAngle, endAngle, color){
 ctx.fillStyle = color;
 ctx.beginPath();
 ctx.moveTo(centerX, centerY);
 ctx.arc(centerX, centerY, radius, startAngle, endAngle);
 ctx.closePath();
 ctx.fill();
}

function drawText(ctx, text, x, y){
   ctx.font = "30px Nunito";
   ctx.strokeText(text, x, y);

}

var PieChart = function(options){
 this.options = options;
 this.canvas = options.canvas;
 this.ctx = this.canvas.getContext("2d");
 this.ctx.filter = "none";
 this.colors = options.colors;

 this.draw = function(){
   var total_value = 0;
   var color_index = 0;
   for(var categ in this.options.data){
    var val  = this.options.data[categ];
    total_value += val;

   }
   
   var start_angle = 180;
   for(categ in this.options.data){
      val = this.options.data[categ];
      var slice_angle = 2 * Math.PI * val / total_value;
      //draw the slice
      drawPieSlice(
         this.ctx,
         this.canvas.width/2,
         this.canvas.height/2,
         Math.min(this.canvas.width/2, this.canvas.height/2),
         start_angle,
         start_angle + slice_angle,
         this.colors[color_index%this.colors.length]
      );
      start_angle += slice_angle;
     color_index++;
   }
   
    if (this.options.doughnutHoleSize){
            drawPieSlice(
                this.ctx,
                this.canvas.width/2,
                this.canvas.height/2,
                this.options.doughnutHoleSize * Math.min(this.canvas.width/2,this.canvas.height/2),
                0,
                2 * Math.PI,
                this.options.color
            );
        }

   if (this.options.text){
       drawText(this.ctx, this.options.text, 
         (this.options.canvas.width /2) - this.options.text.length, this.options.canvas.height/2);
   }

 }
}




function register(){
   
   var request = new XMLHttpRequest()
   request.addEventListener("load", function(){
      console.log("Registered")
   })

   request.open("GET", `http://${window.location.hostname}:8000/register/`)
   request.send(null)
}


function userDashboardHandler(id){
   var canvas = document.getElementById("completion");
   window.setInterval(function(){
      getUserData()
   }, 1000);
}

function refresh(canvas, completion, left){
   var ctx = canvas.getContext("2d");
   ctx.clearRect(0,0,canvas.width, canvas.height);
   
   
   chartData = {
       "completion": completion,
       "left": left
   }
   var myPieChart = new PieChart({
           canvas: canvas,
           data: chartData,
           colors: ["green", "#ddd"],
           doughnutHoleSize: 0.8,
           color: "#fff",
           text: " "+Math.round(((completion/ 6) * 100)) + "%",
   })

   myPieChart.draw();
}

function updateProfile(){
   var cash = document.getElementById('cash');
   var level = document.getElementById('level');
   var response = JSON.parse(this.response);
   cash.innerText =  response.cash;
   level.innerText = response.level;
   completion = response.count;
   left = 6 - completion;
   refresh(document.getElementById('completion'), completion, left);
}


function getUserData(){
   
   id = document.getElementById('user-id').value
   var oReq = new XMLHttpRequest();
   oReq.addEventListener("load", updateProfile);
   oReq.open("GET", `http://${window.location.hostname}:8000/get_data/${id}`);
   oReq.send(null);

   
  
}
/*
function notifyPayment(id){
   socket = new WebSocket('ws://localhost:8000/example/')
   socket.onopen = (event) =>{
       console.log(event)
       data = {
           'id': id,
           'action': 'notify'
       }
       socket.send(JSON.stringify(data));
   }
   
   socket.onmessage = (event) =>{
       
       console.log(event)
   }

   
   socket.onerror = (event) =>{
       console.log(event)
   }
   socket.onclose = (event) =>{
       console.log(event)
   }
}
*/







function markTab(elements){
     var path = window.location.pathname;
    for(var i = 0; i < elements.length; i++){
      if(path.search(elements[i].innerText) > -1){
         elements[i].classList.add('active-btn');
      }
    }
}




function toggleMenu(){
   
   var menu = document.querySelector('.menu')
   if(flagMenu){
      menu.style.display = 'none'
      menu.style.animation = '1s slidein'
      flagMenu = false
   } else{
      menu.style.display = 'block'
      menu.style.animation = '1s slidein'
      flagMenu = true
   }
}




