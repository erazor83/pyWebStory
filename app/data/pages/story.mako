<%include file="page_header.mako"/>

<script type="text/javascript">
	var StoryID="${story_id}";
	var ws_path="${ws_path}";
	var user_name="${user_name}";
	var StoryInfo=${story_info.toJSON()};
</script>
<div id="layout" style="width: 100%; height: 100%;overflow:hidden"></div>

<%include file="page_footer.mako"/>