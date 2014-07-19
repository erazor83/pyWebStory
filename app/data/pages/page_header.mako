<html>
<head>
	<title>PyWebStory</title>
	<script type="application/javascript" src="${js_path}jquery-1.10.2.js"></script>
	<script type="application/javascript" src="${js_path}jquery-ui-1.10.4.custom.min.js"></script>
	<script type="application/javascript" src="${js_path}jquery-dateFormat.min.js"></script>

	<script type="application/javascript" src="${js_path}dump.js"></script>

	<script type="application/javascript" src="${js_path}portal.js"></script>
	<script type="application/javascript" src="${js_path}w2ui.js"></script>
	<script type="application/javascript" src="${js_path}common.js"></script>

	<script type="application/javascript" src="${js_path}jqwidgets/jqxcore.js"></script>
	<script type="application/javascript" src="${js_path}jqwidgets/jqxdata.js"></script>
	<script type="application/javascript" src="${js_path}jqwidgets/jqxmenu.js"></script>
	<script type="application/javascript" src="${js_path}jqwidgets/jqxtree.js"></script>

	<script type="application/javascript" src="${js_path}locale.en.js"></script>

	<link rel="shortcut icon" href="${base_path}images/favicon.ico"/>

	<link rel="stylesheet" type="text/css" href="${css_path}jqwidgets/jqx.base.css" />

	<link rel="stylesheet" type="text/css" href="${css_path}w2ui.css" />
	<link rel="stylesheet" type="text/css" href="${css_path}common.css" />


	<link rel="stylesheet" type="text/css" href="${css_path}font-awesome.css" />

	<!-- dynamic per page js-files -->
% for js_file in js_files:
	<script type="text/javascript" src="${js_file}"></script>
% endfor
	<!-- ------------------------- -->

	<!-- dynamic per page css-files -->
% for css_file in css_files:
	<link rel="stylesheet" type="text/css" href="${css_file}" />
% endfor
	<!-- ------------------------- -->

	<script type="text/javascript">
		var base_path="${base_path}";
		var rpc_path="${base_path}rpc/";
		var URL_INDEX_PAGE="${base_path}";
	</script>

</head>

<html>

<body style="scroll:no;overflow:hidden">
<!--
<div id="background" style="z-index:0">
  <img src="/images/background.jpg" alt="">
</div>
-->

<div id="story_overlay" style="padding-left:30px;display: none; width: 200px; height: 20px; overflow: auto">
	<div rel="body">
		<div style="padding: 10; font-size: 11px">
			<table class="story_overlay_table">
					<tr><th>Title</th><td id="story_overlay_title"> </td></tr>
					<tr><th>Version</th><td id="story_overlay_version"> </td></tr>
					<tr><th>Author</th><td id="story_overlay_author"> </td></tr>
					<tr><th>Copyright</th><td id="story_overlay_copyright"> </td></tr>
					<tr><td colspan="2" id="story_overlay_description"> </td></tr>
			</table>
		</div>
		</div>
</div>

<div id="story_save_overlay" style="padding-left:30px;display: none; width: 250px; height: 20px; overflow: auto">
	<div rel="body">
		<div style="padding: 10; font-size: 11px">
			<table class="story_save_overlay_table">
					<tr><th colspan="2" style="text-align:center">Save</th></tr>
					<tr><th>Name</th><td id="story_save_name"> </td></tr>
					<tr><th>Date</th><td id="story_save_date"> </td></tr>
					<tr><th colspan="2" style="text-align:center">Story</th></tr>
					<tr><th>Title</th><td id="story_save_overlay_title"> </td></tr>
					<tr><th>Version</th><td id="story_save_overlay_version"> </td></tr>
					<tr><td colspan="2" id="story_save_overlay_description"> </td></tr>
			</table>
		</div>
		</div>
</div>

