function toggleGlobalLoadingIndicator() { 
    var spinner_el = $(".spinner");
    if (spinner_el.length == 0) {
        var opts = {
            lines: 13, // The number of lines to draw
            length: 20, // The length of each line
            width: 10, // The line thickness
            radius: 30, // The radius of the inner circle
            corners: 1, // Corner roundness (0..1)
            rotate: 0, // The rotation offset
            direction: 1, // 1: clockwise, -1: counterclockwise
            color: '#000', // #rgb or #rrggbb or array of colors
            speed: 1, // Rounds per second
            trail: 60, // Afterglow percentage
            shadow: false, // Whether to render a shadow
            hwaccel: false, // Whether to use hardware acceleration
            className: 'spinner', // The CSS class to assign to the spinner
            zIndex: 2e9, // The z-index (defaults to 2000000000)
            top: '50%', // Top position relative to parent
            left: '50%' // Left position relative to parent
        };
        $("body").prepend("<div id='spinner-container' style='position:fixed;top:0;right:0;left:0;bottom:0;z-index:9999;overflow:hidden;outline:0;color:#333;background-color:transparent;opacity: 0.8;'></div>")
        var spinner = new Spinner(opts).spin($("#spinner-container")[0]);      
    } else {
        $("#spinner-container").toggleClass("hidden");
    }
}

var isToolOn = false;

$(document).ready(function() {
	// nav header 영역

	$("#logout").on("mouseover", function() {
		$('#logout').addClass('logout_hover');
	}).on("mouseout", function() {
		$('#logout').removeClass('logout_hover');
	});

	$("#logout").on("click", function() {
		$(location).attr('href', '/logout');
	});

	// toolbar 영역
	
	$('#select-all').on("click", function(event) {
		if(this.checked) {
			$(':checkbox').each(function() {
				this.checked = true;
			});
		} else {
			$(':checkbox').each(function() {
				this.checked = false;
			});
		}
	});

	$(".tool").on("mouseover", function() {
		if(!isToolOn) {
			$(this).css("backgroundColor", "#4f5c84");
		}
	}).on("mouseout", function() {
		if(!isToolOn) {
			$(this).css("backgroundColor", "transparent");
		}
	});

	$("#tool-1").on("click", function() {
		if(!isToolOn) {
			toolActivate(1);
			$(".tr-general").animate({
				opacity: 0.3
			}, 750);

			$("html, body").animate({ scrollTop: $(document).height() }, "slow");
			var input_html = "\
				<tr stock-no=\'temp\'> \
	                <td class=\'col-1\'></td> \
	                <td class=\'col-2\'>카테고리</td> \
	                <td class=\'col-3\'><input type=\'text\' class=\'inputform\' name=\'input-name\'></td> \
	                <td class=\'col-4\'><input type=\'text\' class=\'inputform\' name=\'input-size\'></td> \
	                <td class=\'col-5\'><input type=\'text\' class=\'inputform\' name=\'input-stock\'></td> \
	                <td class=\'col-6\'><input type=\'text\' class=\'inputform\' name=\'input-unitcost\'></td> \
	                <td class=\'col-7\'></td> \
	                <td class=\'col-8\'></td> \
	                <td class=\'col-9\'></td> \
	                <td class=\'col-10\'><input type=\'text\' class=\'inputform\' name=\'input-memo\'></td> \
	                <td class=\'col-11\'> \
	                	<img src=\'static/img/s_tool_check.png\' name=\'input-check\' class=\'img-button\'> \
	                	<img src=\'static/img/s_tool_delete.png\' name=\'input-delete\' class=\'img-button\'> \
	                </td> \
	                <td class=\'col-12\'> \
	                </td> \
	            </tr> \
			";
			$("tbody").append(input_html);

			$("tbody").find("input[name=name]").focus();
		}
	});

	$("tbody").on("click", "img[name=input-check]", function() {
		var name = $("input[name=input-name]").val();
		var size = $("input[name=input-size]").val();
		var stock = $("input[name=input-stock]").val();
		var cost = $("input[name=input-unitcost]").val();
		var memo = $("input[name=input-memo]").val()

		$.ajax({
			type: "POST",
			url: "/create/stock",
			data: {
				'name': name,
				'store': $("#storeno").text(),
				'size': size,
				'stock': stock,
				'cost': cost,
				'memo': memo
			},
			dataType: "JSON",
			success: function(data) {
				$("tr[stock-no=temp]").remove();
				var input_html = "\
					<tr class=\'tr-general\' stock-no=\'" + data.stock_no + "\'> \
		                <td class=\'col-1\'><input type=\'checkbox\' class=\'select-one'\></td> \
		                <td class=\'col-2\'>카테고리</td> \
		                <td class=\'col-3\'>" + name + "</td> \
		                <td class=\'col-4\'>" + size + "</td> \
		                <td class=\'col-5\'>" + stock + "</td> \
		                <td class=\'col-6\'>" + cost + "</td> \
		                <td class=\'col-7\'>0</td> \
		                <td class=\'col-8\'>0</td> \
		                <td class=\'col-9\'>" + stock + "</td> \
		                <td class=\'col-10\'>" + memo + "</td> \
		                <td class=\'col-11\'> \
			                <img src='static/img/s_tool_stock.png' name='gene-stock' class='img-button'> \
							<img src='static/img/s_tool_modify.png' name='gene-modify' class='img-button'> \
							<img src='static/img/s_tool_delete.png' name='gene-delete' class='img-button'> \
		                </td> \
		                <td class=\'col-12\'> \
		                </td> \
		            </tr> \
				";
				$("tbody").append(input_html);
							
				$(".tr-general").animate({
					opacity: 1.0
				}, 750);
				toolUnactivate(1);
			},
			error: function(request, status, error) {
				alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error)
			}
		});
	});

	$("tbody").on("click", "img[name=input-delete]", function() {
		$("tr[stock-no=temp]").animate({
			opacity: 0.0
		}, 500, function() {
			$("tr[stock-no=temp]").remove();
		});
		
		$(".tr-general").animate({
			opacity: 1.0
		}, 750);
		toolUnactivate(1);
	});
});

function toolActivate(no) {
	isToolOn = true;

	$("#content table").removeClass("table-hover");
	$("input[type=checkbox]").attr("disabled", true);

	var i;
	for(i = 1; i <= 6; i++) {
		if(i == no) {
			continue;
		} else {
			var obj = $("#toolbar ul").find("img[name=tool-img-" + i + "]");
			var url = obj.attr("src");
			url = url.replace("_on_", "_off_");
			obj.attr("src", url);
		}
	}
}

function toolUnactivate(no) {
	var i;
	for(i = 1; i <= 6; i++) {
		if(i == no) {
			continue;
		} else {
			var obj = $("#toolbar ul").find("img[name=tool-img-" + i + "]");
			var url = obj.attr("src");
			url = url.replace("_off_", "_on_");
			obj.attr("src", url);
		}
	}

	$("input[type=checkbox]").attr("disabled", false);
	$("#content table").addClass("table-hover");
	isToolOn = false;
}

$(document).ajaxStart(function () {
    toggleGlobalLoadingIndicator();
});

$(document).ajaxComplete(function () {
    toggleGlobalLoadingIndicator();
});

/*$(document).ready(function(){

	$("#tool-input").bind("click", function() {
		$("html, body").animate({ scrollTop: $(document).height() }, "slow");
		var input_html = "\
			<tr stock-no='{{ stock[\'no\'] }}'> \
                <td></td> \
                <td>카테고리</td> \
                <td><input type='text' name='name'></td> \
                <td><input type='text' name='size'></td> \
                <td><input type='text' name='stock'></td> \
                <td><input type='text' name='unitcost'></td> \
                <td></td> \
                <td></td> \
                <td><textarea></textarea></td> \
                <td></td> \
                <td> \
                    <button class='btn-confirm btn btn-sm btn-primary'>추가</button> \
                    <button class='bhn-del btn btn-sm btn-primary'>취소</button> \
                </td> \
            </tr> \
		";
		$("table").append(input_html);
	});

	//우클릭 방지, 키 방지, 드래그 방지
	$(document).bind("contextmenu",function(){ return false; });
	$(document).bind('keypress', 'a', function(e){
		if(e.ctrlKey)
			return false;
	});  
  	$(document).mousedown(function(){$(document).mousemove(function(){ return false; }); });  
  	
	$("li.store-name").click(function(){
		$(this).parent().toggleClass('fold');
	});

	$(".btn-edit").click(function(){
		for(var i=0; i<$(this).parent().parent().children().length; i++){
				$(this).parent().parent().children(i).addClass('edit')
		}
	});

	$(".btn-confirm").click(function(){
		for(var i=0; i<$(this).parent().parent().children().length; i++){
				$(this).parent().parent().children(i).removeClass('edit')
		}
	});

	$(".btn-del").live("click", function(){
		var clickedRow = $(this).parent().parent();
		var cls = clickedRow.attr("class");
				 
		// 각 항목의 첫번째 row를 삭제한 경우 다음 row에 td 하나를 추가해 준다.
		if( clickedRow.find("td:eq(0)").attr("rowspan") ){
			if( clickedRow.next().hasClass(cls) ){
				clickedRow.next().prepend(clickedRow.find("td:eq(0)"));
			}
		}
		clickedRow.remove();
 
		// rowspan 조정
		resizeRowspan(cls);
	});
 

	$('#select-all').click(function(event) {
		if(this.checked) {
		// Iterate each checkbox
			$(':checkbox').each(function() {
				this.checked = true;
			});
		} else {
			$(':checkbox').each(function() {
				this.checked = false;
			});
		}
	});

	$('.dropdown-toggle').click(function(){
		$(this).parent().toggleClass('open')
	});

  //우클릭 방지
  $(document).bind("contextmenu",function(){
	  return false;
  });

  //드래그 방지
  $(document).bind("dragstart",function(){
	  return false;
  });
});*/

