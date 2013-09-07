function addportion (item_id, portion){
	$.ajax({
	    url: "/addportion/" + item_id + "/" + portion + "/",
	});
}
