variable "region" {
  default = "us-east-2"
}

variable "availability_zone" {
  default = "us-east-2a"
}

variable "max_spot_price" {
  default = "0.05"
}

variable "instance_type" {
  default = "m4.large"
}

variable "key_name" {
  default = "ds"
}

variable "key_file" {
  default = "key.pem"
}

variable "ami" {
  default = "ami-fcc19b99"
}

variable "ssh_user" {
  default = "ubuntu"
}

provider "aws" {
  region = "${var.region}"
}

resource "aws_spot_instance_request" "ds" {
  spot_price = "${var.max_spot_price}"
  spot_type = "one-time"
  wait_for_fulfillment = true
  availability_zone = "${var.availability_zone}"
  instance_type = "${var.instance_type}"
  key_name = "${var.key_name}"
  ami = "${var.ami}"
  vpc_security_group_ids = ["${aws_security_group.ds.id}"]

  # This hack makes sure the instance is running before Terraform tries to
  # attach the EBS volume.
  provisioner "remote-exec" {
    inline = ["echo"]
  }
  connection {
    user = "${var.ssh_user}"
    private_key = "${file(var.key_file)}"
    agent = false
  }
}

resource "aws_ebs_volume" "ds_workspace" {
  availability_zone = "${var.availability_zone}"
  size = 20
  type = "gp2"
  lifecycle {
    prevent_destroy = true
  }
  tags {
    Name = "ds-workspace"
  }
}

resource "aws_volume_attachment" "ds_workspace" {
  device_name = "/dev/sdf"
  volume_id = "${aws_ebs_volume.ds_workspace.id}"
  instance_id = "${aws_spot_instance_request.ds.spot_instance_id}"

  provisioner "remote-exec" {
    script = "bootstrap.sh"
  }
  connection {
    host = "${aws_spot_instance_request.ds.public_ip}"
    user = "${var.ssh_user}"
    private_key = "${file(var.key_file)}"
    agent = false
  }
}

resource "aws_security_group" "ds" {
  name = "ds"

  # Allow ssh.
  ingress {
    protocol = "tcp"
    from_port = 22
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic.
  egress {
    protocol = "-1"
    from_port = 0
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "ssh" {
  value = "${var.ssh_user}@${aws_spot_instance_request.ds.public_ip}"
}

output "instance_id" {
  value = "${aws_spot_instance_request.ds.spot_instance_id}"
}
