function on_active(id){
          var p = document.getElementById(id);
          var check = document.getElementById(id+'g');
          if (check.checked)
              {p.innerText = "تم";
              check.value = 'True';}
          else {p.innerText = "قيد الانتظار";}
           }