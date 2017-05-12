$(function(){
	
	var worldMap;
	var mouse = { x: 0, y: 0 }
	
	function Map() {
		
		this.WIDTH       = window.innerWidth; 
		this.HEIGHT      = window.innerHeight;  
		
		this.VIEW_ANGLE  = 45;
		this.NEAR        = 0.1; 
		this.FAR         = 10000;
		this.CAMERA_X    = 0;
		this.CAMERA_Y    = 1000;
		this.CAMERA_Z    = 500;
		this.CAMERA_LX   = 0;
		this.CAMERA_LY   = 0;
		this.CAMERA_LZ   = 0;
		
		this.geo;
		this.scene = {};
		this.renderer = {};
		this.projector = {};
		this.camera = {};
		this.stage = {};
		
		this.INTERSECTED = null;
	}
	
	Map.prototype = {
		
		init_d3: function() {

			geoConfig = function() {
				
				this.mercator = d3.geo.equirectangular();
				this.path = d3.geo.path().projection(this.mercator);
				
				var translate = this.mercator.translate();
				translate[0] = 500;
				translate[1] = 0;
				
				this.mercator.translate(translate);
				this.mercator.scale(200);
			}
	
			this.geo = new geoConfig();
		},
		
		init_tree: function() {
			
			if( Detector.webgl ){
				this.renderer = new THREE.WebGLRenderer({
					antialias : true
				});
				this.renderer.setClearColorHex( 0xBBBBBB, 1 );
			} else {
				this.renderer = new THREE.CanvasRenderer();
			}
			
			this.renderer.setSize( this.WIDTH, this.HEIGHT );
			
			this.projector = new THREE.Projector();
			
			// append renderer to dom element
			$("#worldmap").append(this.renderer.domElement);
			
			// create a scene
			this.scene = new THREE.Scene();
			
			// put a camera in the scene
			this.camera = new THREE.PerspectiveCamera(this.VIEW_ANGLE, this.WIDTH / this.HEIGHT, this.NEAR, this.FAR);
			this.camera.position.x = this.CAMERA_X;
			this.camera.position.y = this.CAMERA_Y;
			this.camera.position.z = this.CAMERA_Z;
			this.camera.lookAt( { x: this.CAMERA_LX, y: 0, z: this.CAMERA_LZ} );
			this.scene.add(this.camera);
		},
		
		
		add_light: function(x, y, z, intensity, color) {
			var pointLight = new THREE.PointLight(color);
			pointLight.position.x = x;
			pointLight.position.y = y;
			pointLight.position.z = z;
			pointLight.intensity = intensity;
			this.scene.add(pointLight);
		},
		
		add_plain: function(x, y, z, color) {
			var planeGeo = new THREE.CubeGeometry(x, y, z);
			var planeMat = new THREE.MeshLambertMaterial({color: color});
			var plane = new THREE.Mesh(planeGeo, planeMat);
			
			// rotate it to correct position
			plane.rotation.x = -Math.PI/2;
			this.scene.add(plane);
		},
		
		add_countries: function(data) {

                var country_rates = {
                    AGO: 0.0241535714725,
                    DZA: 0.0558682360675,
                    EGY: 0.0346840520731,
                    NAC: 0.0108785124002,
                    MIC: 0.0517408291473,
                    EUU: 0.0179371216169,
                    BGR: 0.0492782534624,
                    BOL: 0.0306127166224,
                    GHA: 0.00639324497846,
                    PAK: 0.0100240511347,
                    WLD: 0.0359074980433,
                    CPV: 0.0144521876672,
                    PRE: 0.00736965662823,
                    BHS: 0.0845307183468,
                    JOR: 0.0490693551842,
                    LBR: 0.00142663853678,
                    IDX: 0.00376841798437,
                    LBY: 0.144577473652,
                    VNM: 0.0280139038708,
                    TZA: 0.00248787438473,
                    PRT: 0.0659509939979,
                    KHM: 0.00620077093958,
                    SAS: 0.020986125358,
                    PRY: 0.0114925700956,
                    HKG: 0.0999823583689,
                    SAU: 0.325894891909,
                    LBN: 0.0536006385337,
                    BFA: 0.00320559365788,
                    CHE: 0.0249703623135,
                    KEN: 0.0000925531431583,
                    MRT: 0.0120928876634,
                    CHL: 0.0562092620976,
                    CHN: 0.120387454951,
                    KNA: 0.0927826219867,
                    JAM: 0.0366693579165,
                    GIB: 0.250506426124,
                    DJI: 0.00418482214671,
                    GIN: 0.00146449419974,
                    FIN: 0.0962774927387,
                    URY: 0.0100010601614,
                    THA: 0.0822317657671,
                    NPL: 0.00425574619508,
                    MAR: 0.0274551690777,
                    YEM: 0.00545805537301,
                    PHL: 0.0130111240718,
                    ZAF: 0.0609330452781,
                    NIC: 0.00884653253701,
                    LAC: 0.030223252294,
                    SYR: 0.021974475456,
                    MAC: 0.0663337316874,
                    PYF: 0.0471368024568,
                    COD: -0.00214937513592,
                    IRL: 0.0688895568947,
                    DMA: 0.0311334257123,
                    BEN: 0.00934528830512,
                    NGA: 0.00902129251825,
                    BEL: -0.0296217886667,
                    LKA: 0.0103855684555,
                    GBR: -0.0757931594515,
                    GUY: 0.0259298736377,
                    CRI: 0.0235787336893,
                    CMR: 0.00483277176199,
                    LDC: 0.00393678983006,
                    CEB: 0.0231676616485,
                    IDB: 0.0144263950966,
                    HUN: -0.0067094727112,
                    TTO: 0.593918125795,
                    NLD: 0.0701052760193,
                    COM: 0.00295011309798,
                    BMU: 0.0383710052717,
                    MNA: 0.0582163760937,
                    TCD: 0.000528043969725,
                    ROU: 0.0119980298122,
                    MNG: 0.248902487185,
                    BLZ: 0.0193254664244,
                    AFG: 0.0122097270885,
                    GRD: 0.049606461422,
                    GRC: 0.0976968040215,
                    GRL: 0.060004950347,
                    CSS: 0.149984335717,
                    MOZ: -0.00188089676335,
                    OSS: 0.117213617834,
                    SST: 0.114408449387,
                    HTI: 0.00295524951605,
                    BRB: 0.0826592921973,
                    LCA: 0.0390484552273,
                    IND: 0.0249454985193,
                    PSS: 0.0181345475419,
                    SSF: 0.00518546986711,
                    SSA: 0.00517262076996,
                    NOR: 0.152486047821,
                    ATG: 0.0972983008093,
                    FJI: 0.0272965814149,
                    HND: 0.0159853582215,
                    MUS: 0.0507081514741,
                    DOM: 0.0345396328005,
                    LUX: -0.339328323162,
                    ISR: 0.108656298134,
                    PER: 0.0199529662905,
                    IDN: 0.0313957729723,
                    SUR: 0.0461629766783,
                    COG: 0.00649538940644,
                    ISL: -0.0156801911586,
                    GAB: 0.0493852499463,
                    ETH: 0.00182208653949,
                    NER: 0.00185321731155,
                    COL: 0.0169322503135,
                    TMN: 0.0589897312001,
                    IDA: 0.00737459527723,
                    FCS: 0.011565819628,
                    TEA: 0.092474255369,
                    STP: 0.00852959508761,
                    MDG: 0.00105326776061,
                    ECU: 0.0451179928787,
                    SEN: 0.00625448171284,
                    FRA: -0.0140193386921,
                    RWA: 0.000677524297355,
                    GMB: 0.00402595153305,
                    FRO: 0.199793225064,
                    GTM: 0.0101985707475,
                    DNK: 0.00522529762983,
                    AUS: 0.146497460446,
                    AUT: 0.0563535274411,
                    LTE: 0.0941354600697,
                    VEN: -0.0165490260203,
                    TSA: 0.020986125358,
                    IRN: 0.118678702481,
                    PLW: 0.173039883944,
                    LMY: 0.046111486321,
                    LAO: 0.00551739264956,
                    MEA: 0.0944090938631,
                    WSM: 0.02107399499,
                    TUR: 0.068546788707,
                    ALB: 0.00762245090369,
                    MMR: 0.00210208742234,
                    BRN: 0.280010511177,
                    CAN: 0.0521027841722,
                    TUN: 0.0402309596926,
                    LMC: 0.0198938547754,
                    MEX: 0.0433062822098,
                    BRA: 0.0343170272246,
                    OED: 0.0449367775075,
                    UMC: 0.0915990084077,
                    GNQ: 0.126473834403,
                    USA: 0.0073580912885,
                    QAT: 0.693241413202,
                    SWE: -0.0369665037769,
                    GNB: 0.00219507898445,
                    SWZ: 0.0152221815351,
                    TON: 0.0341403342187,
                    CIV: 0.00533391611394,
                    KOR: 0.213137977976,
                    IBT: 0.0451419800036,
                    CAF: 0.000085256647883,
                    CYP: 0.0690750210562,
                    SGP: 0.160707161449,
                    SOM: 0.00061454134982,
                    TSS: 0.00518546986711,
                    POL: 0.0227804885788,
                    HIC: 0.0653794034696,
                    KWT: -0.0505846917665,
                    EAP: 0.0915399282144,
                    EAS: 0.0977761283642,
                    EAR: 0.030478317233,
                    TGO: 0.00528338599251,
                    CYM: 0.147864535635,
                    ARE: 0.350744337583,
                    ESP: 0.0655922606298,
                    IRQ: 0.0714395762942,
                    SLV: 0.0154690685429,
                    MLI: 0.000733827967793,
                    LCN: 0.0324227235511,
                    VCT: 0.0335088270626,
                    MLT: 0.079165755588,
                    HPC: 0.00273334180078,
                    SLE: -0.00254483521065,
                    PAN: 0.0347664089887,
                    SDN: 0.00338333199618,
                    SLB: 0.00490262525564,
                    NZL: 0.052414766114,
                    ITA: 0.0668936832725,
                    JPN: 0.136751992939,
                    TLA: 0.0321711428215,
                    ARB: 0.0765417904972,
                    NCL: 0.0712033662041,
                    PST: 0.0523790242335,
                    ARG: 0.0395249990203,
                    IBD: 0.0609111434561,
                    BHR: 0.379994524673,
                    UGA: 0.00135338705089,
                    PNG: 0.0139527704355,
                    CUB: 0.0291278407004
                };
				var countries = [];
				var i, j;
				
				// convert to threejs meshes
				for (i = 0 ; i < data.features.length ; i++) {
					var geoFeature = data.features[i];
					var properties = geoFeature.properties;
					var feature = this.geo.path(geoFeature);
					
					// we only need to convert it to a three.js path
					var mesh = transformSVGPathExposed(feature);
					
					// add to array
					for (j = 0 ; j < mesh.length ; j++) {
						  countries.push({"data": properties, "mesh": mesh[j]});
					}
				}
				
				// extrude paths and add color
				for (i = 0 ; i < countries.length ; i++) {
		
					// create material color based on average		
					var material = new THREE.MeshPhongMaterial({
						color: this.getCountryColor(countries[i].data, country_rates),
						opacity:0.5
					}); 
							
					// extrude mesh
					var shape3d = countries[i].mesh.extrude({
						amount: 1, 
						bevelEnabled: false
					});

					// create a mesh based on material and extruded shape
					var toAdd = new THREE.Mesh(shape3d, material);
					
					//set name of mesh
					toAdd.name = countries[i].data.name;
					
					// rotate and position the elements
					toAdd.rotation.x = Math.PI/2;
					toAdd.translateX(-490);
					toAdd.translateZ(50);
					toAdd.translateY(20);

					// add to scene
					this.scene.add(toAdd);
				}
		},
		
		getCountryColor: function(data, country_rates) {


//			var multiplier = country_rates[data.iso_a3]*10000;
//
////			for(i = 0; i < 3; i++) {
////				multiplier += data.iso_a3.charCodeAt(i);
////			}
//
//			multiplier = (1.0/366)*multiplier;
//			console.log(multiplier*0xb22222);
//			return multiplier*0xb22222;
            if(data.iso_a3 in country_rates){
                percent = (1+ country_rates[data.iso_a3])*100/1.693241413202;
//                document.getElementById("bufaso").innerHTML = document.getElementById("bufaso").innerHTML + country_rates[data.iso_a3];
                color = '#08a35c';
			    var num = parseInt(color.slice(1),16), amt = Math.round(2.55 * percent), R = (num >> 16) + amt, G = (num >> 8 & 0x00FF) + amt, B = (num & 0x0000FF) + amt;
                return "0x" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);


            } else {
                document.getElementById("bufaso").innerHTML = document.getElementById("bufaso").innerHTML + ' ' + data.iso_a3;

                return 0x333;
            }


		},
		
		setCameraPosition: function(x, y, z, lx, lz) {	
			this.CAMERA_X = x;
			this.CAMERA_Y = y;
			this.CAMERA_Z = z;
			this.CAMERA_LX = lx;
			this.CAMERA_LZ = lz;
		},
		
		moveCamera: function() {
			var speed = 0.2;
			var target_x = (this.CAMERA_X - this.camera.position.x) * speed;
			var target_y = (this.CAMERA_Y - this.camera.position.y) * speed;
			var target_z = (this.CAMERA_Z - this.camera.position.z) * speed;
			
			this.camera.position.x += target_x;
			this.camera.position.y += target_y;
			this.camera.position.z += target_z;
			
			this.camera.lookAt( {x: this.CAMERA_LX, y: 0, z: this.CAMERA_LZ } );
		},
		
		animate: function() {
					
			if( this.CAMERA_X != this.camera.position.x || 
				this.CAMERA_Y != this.camera.position.y || 
				this.CAMERA_Z != this.camera.position.z) {
				this.moveCamera();	
			}
			
			// find intersections
			var vector = new THREE.Vector3( mouse.x, mouse.y, 1 );
			this.projector.unprojectVector( vector, this.camera );
			var raycaster = new THREE.Ray( this.camera.position, vector.subSelf( this.camera.position ).normalize() );
			var intersects = raycaster.intersectObjects( this.scene.children );

			var objects = this.scene.children;

			if ( intersects.length > 1 ) {						
				if(this.INTERSECTED != intersects[ 0 ].object) {
					if (this.INTERSECTED) {
						for(i = 0; i < objects.length; i++) {
							if (objects[i].name == this.INTERSECTED.name) {
								objects[i].material.opacity = 0.5;
								objects[i].scale.z = 1;
							}
						}
						this.INTERSECTED = null;
					}
				}

				this.INTERSECTED = intersects[ 0 ].object;
				for(i = 0; i < objects.length; i++) {
					if (objects[i].name == this.INTERSECTED.name) {
						objects[i].material.opacity = 1.0;
						objects[i].scale.z = 5;
					}
				}

			} else if (this.INTERSECTED) {
				for(i = 0; i < objects.length; i++) {
					if (objects[i].name == this.INTERSECTED.name) {
						objects[i].material.opacity = 0.5;
						objects[i].scale.z = 1;
					}
				}
				this.INTERSECTED = null;
			} 

			this.render();
		},
		
		render: function() {

			// actually render the scene
			this.renderer.render(this.scene, this.camera);
		}
	};

	function init() {
		
		$.when(	$.getJSON("data/countries.json") ).then(function(data){ 
			
			worldMap = new Map();
			
			worldMap.init_d3();
			worldMap.init_tree();
			
			worldMap.add_light(0, 3000, 0, 1.0, 0xFFFFFF);		
			worldMap.add_plain(1400, 700, 30, 0xEEEEEE);
			
			worldMap.add_countries(data);
			
			// request animation frame
			var onFrame = window.requestAnimationFrame;
	
			function tick(timestamp) {
				worldMap.animate();
				
				if(worldMap.INTERSECTED) {
					$('#country-name').html(worldMap.INTERSECTED.name);
				} else {
					$('#country-name').html("move mouse over map");
				}
				
				onFrame(tick);
			}
	
			onFrame(tick);
			
			document.addEventListener( 'mousemove', onDocumentMouseMove, false );
			window.addEventListener( 'resize', onWindowResize, false );
			
		});
	}
	
	function onDocumentMouseMove( event ) {

		event.preventDefault();

		mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
		mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	}
	
	function onWindowResize() {
		
		windowHalfX = window.innerWidth / 2;
		windowHalfY = window.innerHeight / 2;

		worldMap.camera.aspect = window.innerWidth / window.innerHeight;
		worldMap.camera.updateProjectionMatrix();

		worldMap.renderer.setSize( window.innerWidth, window.innerHeight );
	}

	$('.navbar-fixed-top ul li a').click(function() {		
		switch (this.hash) {
		   case "#africa":
			  worldMap.setCameraPosition(100, 320, 200, 100, 50);
			  break;
		   case "#europe":
			  worldMap.setCameraPosition(75, 210, -75, 75, -150);
			  break;
		   case "#asia":
			  worldMap.setCameraPosition(400, 350, 100, 400, -100);
			  break;
		   case "#northamerica":
			  worldMap.setCameraPosition(-300, 350, -90, -300, -120);
			  break;
		   case "#southamerica":
		   	  worldMap.setCameraPosition(-200, 350, 250, -200, 120);
			  break;
		   case "#australia":
			  worldMap.setCameraPosition(500, 270, 300, 500, 120);
			  break;
		   case "#all":
			  worldMap.setCameraPosition(0, 1000, 500, 0, 0);
			  break;
		}
	});
	
	window.onload = init;
		
}());