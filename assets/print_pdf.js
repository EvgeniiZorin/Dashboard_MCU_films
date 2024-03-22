function printData() {
  var divToPrint=document.getElementById("main_container");

  newWin= window.open("");

  newWin.document.write(divToPrint.outerHTML);

  newWin.print();

  newWin.close();
}

setTimeout(function mainFunction(){
  try {
      document.getElementById("run").addEventListener("click", function(){
          printData();
      })
    }
    catch(err) {
      console.log(err)
    }
  console.log('Listener Added!');
}, 30000);
