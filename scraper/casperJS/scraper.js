var casper = require('casper').create({
    logLevel: "debug"
});

casper.on('remote.message', function(message) {
    this.echo(message);
});

var list = "აა"

casper.start('http://www.aljyyosh.org/archive.php', function() {
    list = this.evaluate(function() {
    	//console.log('aa')
        table = document.getElementById("ldeface")
        //console.log(table.rows.length)
        //console.log(table.rows[0])
        res = new Array(table.rows.length)
        for (var i = 0, row; row = table.rows[i]; i++) {
        	//console.log(i)
	   		var temp = new Array()
		 	for (var j = 0, col; col = row.cells[j]; j++) {
		 		//console.log(col.innerHTML)
		    	temp.push(col.innerHTML)
		   }
		   	res[i] = temp
		}
		console.log(res.length)
		return res
    });
});

casper.then(function () {
	for(l in list){
		//this.echo(list[l][list[l].length-1])
		this.echo(list[l])
	}
});

casper.run();