function page(){

 $('table.paginated').each(function() {

  var pagesu = 10;  //페이지 번호 갯수

  var currentPage = 0;

  var numPerPage = 20;  //목록의 수

  var $table = $(this);

  var pagination = $("#pagination");



  //length로 원래 리스트의 전체길이구함

  var numRows = $table.find('tbody tr').length;



  //Math.ceil를 이용하여 반올림

  var numPages = Math.ceil(numRows / numPerPage);



  //리스트가 없으면 종료

  if (numPages==0) return;



  //pager라는 클래스의 div엘리먼트 작성

  var $pager = $('<div class="pager"></div>');

  var nowp = currentPage;

  var endp = nowp+10;



  //페이지를 클릭하면 다시 셋팅

  $table.bind('repaginate', function() {

   //기본적으로 모두 감춘다, 현재페이지+1 곱하기 현재페이지까지 보여준다

   $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();

   $("#pagination").html("");



   if (numPages > 1) {     // 한페이지 이상이면

    if (currentPage < 5 && numPages-currentPage >= 5) {   // 현재 5p 이하이면

     nowp = 0;     // 1부터

     endp = pagesu;    // 10까지

    }else{

     nowp = currentPage -5;  // 6넘어가면 2부터 찍고

     endp = nowp+pagesu;   // 10까지

     pi = 1;

    }

    if (numPages < endp) {   // 10페이지가 안되면

     endp = numPages;   // 마지막페이지를 갯수 만큼

     nowp = numPages-pagesu;  // 시작페이지를   갯수 -10

    }

    if (nowp < 1) {     // 시작이 음수 or 0 이면

     nowp = 0;     // 1페이지부터 시작

    }

   }else{       // 한페이지 이하이면

    nowp = 0;      // 한번만 페이징 생성

    endp = numPages;

   }



   // [처음]

   $('<span class="pageNum first">처음</span>').bind('click', {newPage: page},function(event) {

    currentPage = 0;

    $table.trigger('repaginate');

    $($(".pageNum")[2]).addClass('active').siblings().removeClass('active');

   }).appendTo(pagination).addClass('clickable');



   // [이전]

   $('<span class="pageNum back">이전</span>').bind('click', {newPage: page},function(event) {

    if(currentPage == 0) return;



    currentPage = currentPage-1;

    $table.trigger('repaginate');

    $($(".pageNum")[(currentPage-nowp)+2]).addClass('active').siblings().removeClass('active');

   }).appendTo(pagination).addClass('clickable');



   // [1,2,3,4,5,6,7,8]

   for (var page = nowp ; page < endp; page++) {

    $('<span class="pageNum"></span>').text(page + 1).bind('click', {newPage: page}, function(event) {

     currentPage = event.data['newPage'];

     $table.trigger('repaginate');

     $($(".pageNum")[(currentPage-nowp)+2]).addClass('active').siblings().removeClass('active');

    }).appendTo(pagination).addClass('clickable');

   }



   // [다음]

   $('<span class="pageNum next">다음</span>').bind('click', {newPage: page},function(event) {

    if(currentPage == numPages-1) return;



    currentPage = currentPage+1;

    $table.trigger('repaginate');

    $($(".pageNum")[(currentPage-nowp)+2]).addClass('active').siblings().removeClass('active');

   }).appendTo(pagination).addClass('clickable');



   // [끝]

   $('<span class="pageNum last">끝</span>').bind('click', {newPage: page},function(event) {

    currentPage = numPages-1;

    $table.trigger('repaginate');

    $($(".pageNum")[endp-nowp+1]).addClass('active').siblings().removeClass('active');

   }).appendTo(pagination).addClass('clickable');



   $($(".pageNum")[2]).addClass('active');

  });



  $pager.insertAfter($table).find('span.pageNum:first').next().next().addClass('active');

  $pager.appendTo(pagination);

  $table.trigger('repaginate');

 });

}



$(function(){

  // table pagination

  page();

});
