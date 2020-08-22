
/**
 * Handle the admin dashboard
 * Live update in realtime
 */

 
document.addEventListener("DOMContentLoaded", function(){

   var active_id = document.getElementById('active-m').value
   var activeTab = document.getElementById(active_id)
   activeTab.classList.add('active-tab');
   

})

function dashboardHandler(){
    var users = document.getElementById("users-count")
    var active = document.getElementById('active')
    var not_active = document.getElementById('not-active')
    var completed_level1 = document.getElementById('levels-1')
    var completed_level2 = document.getElementById('levels-2')
    var withdrawals = document.getElementById('withdrawals')
    var pending_withdrawals = document.getElementById('pending-withdrawals')
    var completed_withdrawals = document.getElementById('completed-withdrawals')
    var logger = document.getElementById("logger");
   
    var request = new XMLHttpRequest()
 
    request.addEventListener("load", function(){
        var data = JSON.parse(this.response)
        console.log(data)
        users.innerText = data.users
        active.innerText = data.active
        not_active.innerText = data.not_active
        completed_level1.innerText = data.level1
        completed_level2.innerText = data.level2
        withdrawals.innerText = data.payments
        pending_withdrawals.innerText = data.pending
        completed_withdrawals.innerText = data.completed
        dataprofiles = {
           'active': data.active,
           'notactive': data.not_active,
           'level1': data.level1,
           'level2': data.level2
        }
        datawithdrawals = {
           'pending': data.pending,
           'completed': data.completed
        }
 
        
        profiles = new PieChart({
          canvas: document.getElementById("user-profiles"),
          data: dataprofiles,
          colors: ["#FFD700", "purple", "#F5B041", "teal"],
          doughnutHoleSize: 0.8,
          color: "#fff",
       })
       profiles.draw()
 
       withdrawals = new PieChart({
          canvas: document.getElementById("w"),
          data: datawithdrawals,
          colors: ["#EB984E", "#82E0AA"],
          doughnutHoleSize: 0.8,
          color: "#fff",
       })
 
       withdrawals.draw()
 
    })
    
    request.open("GET", `http://${window.location.hostname}/get_dashboard_data`)
    request.send(null)
   
 }

 /*Update table data when a user searches for data*/

 function updateTable(data){
   
    tabledata = document.querySelectorAll('tr');
    for(var i = 0; i < tabledata.length; i++){
       tabledata[i].remove();
    }
 
    table = document.querySelector('table');
    var head = document.createElement('tr');
    var first = document.createElement('th');
    first.innerText = "Firstname"
    var second  = document.createElement('th');
    second.innerText = "Lastname"
    var third = document.createElement('th');
    third.innerText = 'Country'
    var fourth = document.createElement('th')
    fourth.innerText = 'Phone'
    var fifth = document.createElement('th')
    fifth.innerText = 'Level'
    var sixth = document.createElement('th')
    sixth.innerText = 'Date joined'
    var seventh = document.createElement('th')
    seventh.innerText = 'Action'
 
    head.appendChild(first);
    head.appendChild(second)
    head.appendChild(third)
    head.appendChild(fourth)
    head.appendChild(fifth)
    head.appendChild(sixth)
    head.appendChild(seventh)
    head.appendChild(document.createElement('th'))
    head.appendChild(document.createElement('th'))
    head.classList.add('table-titles')
    table.appendChild(head)
   
 
 
    head = JSON.parse(response.data);
    console.log(data);
    var id = 0;
    for(var i = 0; i < data.length; i++){
 
       
       var tr = document.createElement('tr');
 
       var firstname = document.createElement('td')
       firstname.innerHTML = `<span class='hidden'>Firstname:</span>${data[i].fields.first_name}`
 
       var lastname = document.createElement('td')
       lastname.innerHTML = `<span class='hidden'>Lastname:</span>${data[i].fields.last_name}`
 
       var country = document.createElement('td')
       country.innerHTML = `<span class='hidden'>Country:</span>${data[i].fields.country}`

 
       var phone = document.createElement('td')
       phone.innerHTML = `<span class='hidden'>Phone:</span>${data[i].fields.phone}`
 
       var level = document.createElement('td')
       level.innerHTML = `<span class='hidden'>Level:</span>${data[i].fields.level}`
       
       var dateJoined = document.createElement('td')
       dateJoined.innerHTML = `<span class='hidden'>Date joined:</span>${data[i].fields.date_joined}`

       var action = document.createElement('td')
       action.classList.add('edit')
       var viewProfile = document.createElement('td')
       viewProfile.classList.add('edit')
       viewProfile.innerHTML = `<a class="view-profile" href="/view/details/${data[i].pk}">Profile</a>`
       var deleteProfile = document.createElement('td')
       deleteProfile.classList.add('edit')
       deleteProfile.innerHTML = `<button class = 'del-btn' onclick = "deleteUser(${data[i].pk})">Delete</button>`
       id = data[i].pk
       
       if(data[i].fields.is_active == true){
          action.innerHTML = `<button id = 'btn${id}' class='orange' onclick='activateProfile(${data[i].pk})'>Deactivate</button> `
       } else if(data[i].fields.is_active == false){
          action.innerHTML = `<button id = 'btn${id}' class='blue' onclick='activateProfile(${data[i].pk})'>Activate</button> `
       }
 
       
 
       tr.appendChild(firstname)
       tr.appendChild(lastname)
       tr.appendChild(country)
       tr.appendChild(phone)
       tr.appendChild(level)
       tr.appendChild(dateJoined)
       tr.appendChild(action)
       tr.appendChild(viewProfile)
       tr.appendChild(deleteProfile)
       table.appendChild(tr)
 
    }
 }

 /**
  * Search for a  user in the database
  */
 
function submitAjax(){
    formdata = new FormData()
    var search = document.getElementById('search').value;
    
 
    var request = new XMLHttpRequest();
    
    request.addEventListener("load", function(){
       console.log(this.response);
       response = JSON.parse(this.response);
       var data = JSON.parse(response.data);
       updateTable(data)
 
    });
 
    
 
    request.open("GET",`http://${window.location.hostname}:8000/search/name/${search}`)
    request.send(null)
 }


 /**
  * Filter users based on a property
  */
 
function initSelectors(){
    var activity = document.getElementById('activity');
    var country = document.getElementById('country');
    activity.addEventListener('change', function(){
       var request = new XMLHttpRequest();
       request.addEventListener('load', function(){
          response = JSON.parse(this.response)
          var data = JSON.parse(response.data)
          if(data !== undefined)
             updateTable(data);
          else
              alert("Something went wrong could not retrieve data") 
       })
 
       request.open("GET", `http://${window.location.hostname}:8000/search/activity/${activity.value}`)
       request.send(null)
 
    })
 
    country.addEventListener('change', function(){
       var request = new XMLHttpRequest();
       request.addEventListener('load', function(){
          response = JSON.parse(this.response)
          var data = JSON.parse(response.data)
          if(data !== undefined)
             updateTable(data);
          else
              alert("Something went wrong could not retrieve data") 
       })
 
       request.open("GET", `http://${window.location.hostname}:8000/search/country/${country.value}`)
       request.send(null)
 
    })
 
 }

/**
 * Get payments
 * @param {String} type 
 */ 
function getPayments(type){
    var pendingButton = document.getElementById('pending')
    var completedButton = document.getElementById('completed')
   if(type =='completed'){
      pendingButton.classList.remove('active')
      completedButton.classList.add('active')
   } else{
      completedButton.classList.remove('active')
      pendingButton.classList.add('active')
   }
   var request = new XMLHttpRequest();
   request.addEventListener('load', function(){
      response = JSON.parse(this.response)
      console.log(response)
      data = response.data
      console.log(data)
      if(data !== undefined)
        {
           //Update our table
           table = document.querySelector('.payments-table');
           tabledata = document.querySelectorAll('.payments-table tr');
           for(var i = 0; i < tabledata.length; i++){
              tabledata[i].remove()
           }
          //Recreate the table
          var head = document.createElement('tr')
          var first = document.createElement('th')
          first.innerText = 'Bank'
          var second = document.createElement('th')
          second.innerText = 'Account number'
          var third = document.createElement('th')
          third.innerText = 'Name'
          var fourth = document.createElement('th')
          fourth.innerText = 'Surname'
          var fifth = document.createElement('th')
          fifth.innerText = 'Balance'
          var sixth = document.createElement('th')
          sixth.innerText = 'Action'

          //append the titles to the head row
          head.appendChild(first)
          head.appendChild(second)
          head.appendChild(third)
          head.appendChild(fourth)
          head.appendChild(fifth)
          head.appendChild(sixth)
          head.appendChild(document.createElement('th'))
         //append the head row to the table
         table.appendChild(head)


         for(var i = 0; i < data.length; i++){
            pdata = data[i]
             var tablerow = document.createElement('tr')
             tablerow.id = "row"+pdata.pk
             var bank = document.createElement('td')
             bank.innerHTML = pdata.bank
             var accountNumber = document.createElement('td')
             accountNumber.innerText = pdata.accountNumber
             var name = document.createElement('td')
             name.innerText = pdata.firstname
             var surname = document.createElement('td')
             surname.innerText = pdata.surname
             var balance = document.createElement('td')
             balance.innerText = pdata.balance
             var action = document.createElement('td')
             action.classList.add('edit')
             var commit = document.createElement('td')
             commit.classList.add('edit')
             commit.innerHTML = `<button class='done' onclick='paymentDone(${pdata.pk})'>Commit</button>` 
             action.innerHTML = `<a class='view-profile' href='/view/details/${pdata.id}'>Profile</a>`;
             
            


             //append data to the tablerow
             tablerow.appendChild(bank)
             tablerow.appendChild(accountNumber)
             tablerow.appendChild(name)
             tablerow.appendChild(surname)
             tablerow.appendChild(balance)
             tablerow.appendChild(action)
             if(type == 'pending'){
                tablerow.appendChild(commit)
             }
            //append tablerow to the table
            table.appendChild(tablerow)
         }
        }
   })
   request.open("GET", `http://${window.location.hostname}:8000/get_payments/${type}`)
   request.send(null)
}

/**
 * Pay a user
 * @param {Integer} pk 
 */
function paymentDone(pk){
   var request = new XMLHttpRequest()
   request.addEventListener("load", function(){
      var row = document.getElementById("row"+pk);
      row.remove();
   })
   request.open("GET", `https://localhost:8000/pay/${pk}`)
   request.send(null)
}

function fireAdmin(id){
   var request = new XMLHttpRequest()
   request.addEventListener("load", function(){
      var row = document.getElementById("row"+id)
      row.remove()
   })
   request.open("GET", `http://${window.location.hostname}:8000/fire/${id}`)
   request.send(null)
}

function deleteUser(id){
   var request = new XMLHttpRequest()
   request.addEventListener("load", function(){
      console.log(this.response)
      response = JSON.parse(this.response)
      var dialog = document.querySelector('.dialog');
      dialog.style.display = 'block'
      var messenger = document.querySelector('#message-delete-user')
      messenger.innerText = response.message
      if(response.code == 1){
         var row = document.querySelector("#row"+id)
         row.remove()
      }
   })
   request.open("GET", `http://${window.location.hostname}:8000/delete_user/${id}`)
   request.send(null)
}

function closeDialog(){
   var dialog = document.querySelector('.dialog')
   dialog.style.display = 'none';
}

function inflateList(){
   var request = new XMLHttpRequest();
   request.addEventListener("load", function(){
      var addAdminDialog = document.querySelector('.add-admin-dialog')
      addAdminDialog.style.display = "block";
      data = JSON.parse(this.response)
      users = JSON.parse(data.users)
      console.log(users)
      var list = document.querySelector('#user-list')
      list.innerHTML = ""
      for(var i = 0; i < users.length; i++){
         list.innerHTML += `<li id = 'item${users[i].pk}'>${users[i].fields.username} <button onclick=addAdmin(${users[i].pk})>+</button></li>`
      }
   })  
   request.open("GET", `http://${window.location.hostname}:8000/get_admins`)
   request.send(null)
}

function closeAddAdminDialog(){
   var addAdminDialog = document.querySelector('.add-admin-dialog')
   addAdminDialog.style.display = 'none';
}

function addAdmin(id){
   var request = new XMLHttpRequest()
   request.addEventListener("load", function(){
      var item = document.getElementById('item'+id)
      var mResponse = JSON.parse(this.response)
      if(mResponse.code == 1){
         item.remove()
      }else{
         var error_message = document.querySelector("#error-msg")
         error_message.innerText = mResponse.message
      }
      
   })
   request.open("GET", `http://${window.location.hostname}:8000/make_admin/${id}`)
   request.send(null)
}