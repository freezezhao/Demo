function D4demo(){		
	
	var QingStor = require('qingstor-sdk').QingStor;
	var config = require('qingstor-sdk').Config;
	let userConfig = new config('WPGRBWCXMDVULWPJXZCX','RHw27p6DfSZMwWIPpMuPjAXYmeWN53FhSdsjpKzQ');
	var x=document.getElementById("video_file");
	var result = document.getElementById("result");
	var service = new QingStor(userConfig);
	service.listBuckets({
		'location': 'sh1a'
		}, function(err, data) {
		console.log(res.statusCode)
		console.log(res.buckets);
		alert(res.buckets);
	});
	bucket = service.Bucket('zhenjing', 'sh1a');
	var myreader = new FileReader();
	var y = document.getElementById("video_file").files[0];
	myreader.readAsDataURL(y);
	myreader.onload=function(e){
		var result=document.getElementById("result");
		result.innerHTML='<img src="' + this.result +'" alt="" />'; 
		bucket.putObject('object', {
			'body': this.result
			}, function(err, data) {
			alert(res.statusCode);
			alert(x.type);
		});
	}	
	
}






