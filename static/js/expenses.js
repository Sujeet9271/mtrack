function _delete(url){
    bootbox.confirm("Confirmation to delete?", function(result){
       if(result){
           window.location.href=url
           }
    });
   }
   function _edit(url){
    bootbox.confirm("Confirmation to edit?", function(result){
       if(result){
           window.location.href=url
           }
    });
   }

   $('.accordion-toggle').click(function(){
   $('.hiddenRow').hide();
   $(this).next('tr').find('.hiddenRow').show();
   });

function searchTable() {
var input, filter, found, table, tr, td, i, j;
input = document.getElementById("myInput");
filter = input.value.toUpperCase();
table = document.getElementById("expensebody");
tr = table.getElementsByTagName("tr");
for (i = 0; i < tr.length; i++) {
td = tr[i].getElementsByTagName("td");
for (j = 0; j < td.length; j++) {
 if (td[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
   found = true;
 }
}
if (found) {
 tr[i].style.display = "";
 found = false;
} else {
 tr[i].style.display = "none";
}
}
var cls = document.getElementById("expensebody").getElementsByTagName("td");
var sum = 0;
for (var i = 0; i < cls.length; i++) {
// Here you check if it's a countable class and the parent tr's style is a visible tr
if (cls[i].className == "amount" && cls[i].closest("tr").style.display != "none") {
 sum += isNaN(cls[i].innerHTML) ? 0 : parseFloat(cls[i].innerHTML);
}
}
document.getElementById('total').innerHTML = sum;

}
var cls = document.getElementById("expensebody").getElementsByTagName("td");
var sum = 0;
for (var i = 0; i < cls.length; i++) {
if (cls[i].className == "amount") {
sum += isNaN(cls[i].innerHTML) ? 0 : parseInt(cls[i].innerHTML);
}
}
document.getElementById('total').innerHTML += sum;

//for filter button
function filter() {
   var x = document.getElementById("filter");
   // document.getElementById("filterbutton").value="Clear";
   
   if (x.style.display === "none") {
       x.style.display = "block";           
       
       
   } else {
       x.style.display = "none"; 
        
              
                  
   }
   }
   function cleardate(){
       document.getElementById("from_date").value="";
       document.getElementById("to_date").value=""; 
       datefilter.submit();
   }