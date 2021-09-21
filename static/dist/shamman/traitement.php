<?php 
namespace Home;
require '../../../core/root/includes.php';
use Native\RESPONSE;
extract($_POST);

$data = new RESPONSE;

if ($action == "session") {
	session($name, $value);
}


if ($action == "unsetSession") {
	unset_session($name);
}


if ($action == "getSession") {
	return getSession($name);
}



if ($action === "save-formShamman") {
	$class = TABLE::fullyClassName($classname);
	if (class_exists($class)) {
		$item = new $class();
		$item->hydrater($_POST);
		$files = [];
		if (isset($_FILES)) {
			foreach ($_FILES as $key => $value) {
				if ($key !== "id" && $value != "") {
					$files[] = $value;
				}
			}
		}
		if ($item->id != null) {
			$item->sentenseUpdate();
			$data = $item->save();
			$item->uploading($files);
		}else{
			$item->files = $files;
			$data = $item->enregistre();
		}
	}else{
		$data->status = false;
		$data->message = "Erreur lors du processus. Veuillez recommencer !";
	}
	echo json_encode($data);
}



//disponiblité des elements
if ($action === "enable") {
	$class = TABLE::fullyClassName($table);
	if (class_exists($class)) {
		$datas = $class::findBy(["id ="=>$id]);
		if (count($datas) == 1) {
			$element = $datas[0];
			$element->actualise();
			if ($element->enable == 1) {
				$element->enable = 0;
			}else{
				$element->enable = 1;
			}
			$data = $element->save();
		}		
	}else{
		$data->status = false;
		$data->message = "Erreur lors du changement de disponiblité de l'element !";
	}
	echo json_encode($data);
}




//annulation d'un element
if ($action === "annuler") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$class = TABLE::fullyClassName($table);
			if (class_exists($class)) {
				$element = new $class();
				$element->setId($id);
				$element->actualise();
				$data = $element->annuler();
			}else{
				$data->status = false;
				$data->message = "Erreur lors de la suppression de l'element !";
			}
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}


//disponiblité des elements
if ($action === "changeActive") {
	$class = TABLE::fullyClassName($table);
	if (class_exists($class)) {
		$datas = $class::findBy(["id ="=>$id]);
		if (count($datas) == 1) {
			$element = $datas[0];
			$element->actualise();
			if ($element->isActive == TABLE::OUI) {
				$element->isActive = TABLE::NON;
			}else{
				$element->isActive = TABLE::OUI;
			}
			$data = $element->save();
		}		
	}else{
		$data->status = false;
		$data->message = "Erreur lors du changement de disponiblité de l'element !";
	}
	echo json_encode($data);
}





//modification des elements
if ($action == "get_data") {
	$data = new RESPONSE;
	$class = TABLE::fullyClassName($table);
	if (class_exists($class)) {
		$datas = $class::findBy(["id ="=>$id]);
		if (count($datas) == 1) {
			$data = $datas[0];
			$data->status = true;

			if ($table == "productionchantier") {
				$data->fourni("ligneproductionchantier");
				foreach ($data->ligneproductionchantiers as $key => $value) {
					$prod = "prod-".$value->produit_id;
					$data->$prod = $value->quantite;
				}

				$data->fourni("ligneconsommationchantier");
				foreach ($data->ligneconsommationchantiers as $key => $value) {
					$conso = "conso-".$value->ressource_id;
					$data->$conso = $value->quantite;
				}
			}

		}
	}else{
		$data->status = false;
		$data->message = "Une erreur s'est produite, veuillez recommencer !";
	}
	echo json_encode($data);
}


//suppression des elements
if ($action === "suppression") {
	$class = TABLE::fullyClassName($table);
	if (class_exists($class)) {
		$element = new $class();
		$element->setId($id);
		$data = $element->supprime();
	}else{
		$data->status = false;
		$data->message = "Erreur lors de la suppression de l'element !";
	}
	echo json_encode($data);
}


//suppression des elements avec mot de passe
if ($action === "verifierPassword") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$data->status = true;
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}



//veroouiller un user
if ($action === "lock") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$class = TABLE::fullyClassName($table);
			if (class_exists($class)) {
				$element = new $class();
				$element->setId($id);
				$element->actualise();
				$data = $element->lock();
			}else{
				$data->status = false;
				$data->message = "Erreur lors de la suppression de l'element !";
			}
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}


//veroouiller un user
if ($action === "resetPassword") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$class = TABLE::fullyClassName($table);
			if (class_exists($class)) {
				$element = new $class();
				$element->setId($id);
				$element->actualise();
				$data = $element->resetPassword();
			}else{
				$data->status = false;
				$data->message = "Erreur lors de la suppression de l'element !";
			}
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}



//reinitialiser le mot de passe
if ($action === "unlock") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$class = TABLE::fullyClassName($table);
			if (class_exists($class)) {
				$element = new $class();
				$element->setId($id);
				$element->actualise();
				$data = $element->unlock();
			}else{
				$data->status = false;
				$data->message = "Erreur lors de la suppression de l'element !";
			}
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}



//suppression des elements avec mot de passe
if ($action === "suppression_with_password") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$class = TABLE::fullyClassName($table);
			if (class_exists($class)) {
				$element = new $class();
				$element->setId($id);
				$data = $element->supprime();
			}else{
				$data->status = false;
				$data->message = "Erreur lors de la suppression de l'element !";
			}
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}


//delete des elements
if ($action === "delete_suppression") {
	$class = TABLE::fullyClassName($table);
	if (class_exists($class)) {
		$element = new $class();
		$element->setId($id);
		$data = $element->delete();
	}else{
		$data->status = false;
		$data->message = "Erreur lors de la suppression de l'element !";
	}
	echo json_encode($data);
}


if ($action === "delete_with_password") {
	$datas = EMPLOYE::findBy(["id = "=>getSession("employe_connecte_id")]);
	if (count($datas) > 0) {
		$employe = $datas[0];
		$employe->actualise();
		if ($employe->checkPassword($password)) {
			$class = TABLE::fullyClassName($table);
			if (class_exists($class)) {
				$element = new $class();
				$element->setId($id);
				$data = $element->delete();
			}else{
				$data->status = false;
				$data->message = "Erreur lors de la suppression de l'element !";
			}
		}else{
			$data->status = false;
			$data->message = "Votre mot de passe ne correspond pas !";
		}
	}else{
		$data->status = false;
		$data->message = "Vous ne pouvez pas effectué cette opération !";
	}
	echo json_encode($data);
}


if ($action === "session__") {
	session($name, $value);
	echo ($name == "last_access" && is_null(getSession("page_session")));
	if ($name == "last_access" && is_null(getSession("page_session"))) {
		session($name, time());
	}
}



if ($action === "params") {
	$params = PARAMS::findLastId();
	echo json_encode($params);
}