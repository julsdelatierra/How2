<?php
defined( '_JEXEC' ) or die( 'Restricted access' );
JPlugin::loadLanguage( 'tpl_SG1' );
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $this->language; ?>" lang="<?php echo $this->language; ?>" >
<head>
<title><?php mosShowHead(); ?></title>
<link rel="shortcut icon" href="templates/<?php echo $this->template ?>/favicon.ico" />
<link rel="stylesheet" href="templates/system/css/system.css" type="text/css" />
<link rel="stylesheet" href="templates/<?php echo $this->template ?>/css/template.css" type="text/css" />
<script src="http://www.hdi.com.mx/scripts/js_flash.js" language="JavaScript" type="text/javascript"></script>
<!--[if lte IE 7]>
<link rel="stylesheet" href="templates/<?php echo $this->template ?>/css/ie7.css" type="text/css" />
<![endif]-->


<script language="JavaScript">
<!--
// Codigo para los botones del menu superior
// Creamos los objetos de la clase Image

image0 = new Image();

image1 = new Image();

image2 = new Image();

image3 = new Image();

image4 = new Image();

image5 = new Image();

// Fin de esta onda
-->
</script>

</head>
<body>
	<div id="fix">
	<div id="header">
		<div class="menujceb">
		  <div id="logotipo">
		  </div>
		  <div id="contratacion">
		  </div>
		  <div id="user_login">
		    <jdoc:include type="modules" name="usuario" />
		  </div>
		</div>
		<div id="animacion">
			<object width="550" height="210"><param name="movie" value="templates/<?php echo $this->template ?>/images/animacion.swf"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="templates/<?php echo $this->template ?>/images/animacion.swf" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="550" height="210"></embed></object>
		</div>
	</div>
	
	<div id="main_menu">
		<br />
		<jdoc:include type="modules" name="menuhoriz" />
	</div>
	</div>
	<div id="scroll">
	<div class="center">	
		<div id="wrapper">
			<div id="content">
				<div id="maincolumn">	
					<div class="nopad">
						<jdoc:include type="message" />
						<?php if($this->params->get('showComponent')) : ?>
							<jdoc:include type="component" />
						<?php endif; ?>
					</div>
				</div>		
			</div>
			<div id="contentbottom">
				<jdoc:include type="modules" name="enlaces" />
			</div>
		</div>
	</div>
	<div id="footer">
		<p style="color:white; font-weight:bold; text-align:center;">Soportador por <a href="http://www.wmid.com" style="color:white; font-weight:bold;">wmid</a> 2010.</p>
	</div>
	</div>
<!-- Woopra Code Start -->
<script type="text/javascript" src="//static.woopra.com/js/woopra.v2.js"></script>
<script type="text/javascript">
woopraTracker.track();
</script>
<!-- Woopra Code End -->
</body>
</html>