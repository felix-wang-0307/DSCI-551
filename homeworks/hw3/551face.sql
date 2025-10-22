drop schema if exists 551face;
create schema 551face;

use 551face;

drop table if exists download;
drop table if exists file;
drop table if exists model;
drop table if exists user;

-- users
create table user (id varchar(20) primary key, 
		name text, email text);
insert into user values('u1', 'john smith', 'john@usc.edu');
insert into user values('u2', 'david chu', 'david@ucla.edu');
insert into user values('u3', 'mariana kelly', 'kelly@caltech.edu');

-- num_params: number of parameters in million
-- user_id: the id of user who contributes and owns the model
-- note: each model is owned by exactly one user. 
create table model (id varchar(20) primary key, name text, 
	task text, 
	num_params float, 
    user_id varchar(20) not null,
    foreign key (user_id) references user(id));
insert into model values('m1', 'gpt-2', 'language generation',
	137, 'u1');
    
-- size: file size in MB
create table file (id varchar(20) primary key, 
		file_path text, size float,
		model_id varchar(20) not null, 
        foreign key (model_id) references model(id));
insert into file values('f1', '/llm/gpt-2/model.safetensors', 548, 'm1');
insert into file values('f2', '/llm/gpt-2/tokenizer.json', 1.36, 'm1');

-- tracking downloads of files by users
create table download(user_id varchar(20), file_id varchar(20),
	primary key (user_id, file_id),
    foreign key (user_id) references user(id),
    foreign key (file_id) references file(id));
insert into download values('u1', 'f1');
insert into download values('u1', 'f2');
insert into download values('u2', 'f1');

-- insert more data
-- More users
insert into user values('u4', 'sofia ramirez', 'sofia@mit.edu');
insert into user values('u5', "liam o\'connor", 'liam@stanford.edu');
insert into user values('u6', 'emily wong', 'emily@berkeley.edu');
insert into user values('u7', 'aarav patel', 'aarav@harvard.edu');

-- More models (each owned by one user)
insert into model values('m2', 'bert-base', 'language understanding', 110, 'u2');
insert into model values('m3', 'vit-large', 'image classification', 307, 'u3');
insert into model values('m4', 'whisper-small', 'speech recognition', 244, 'u4');
insert into model values('m5', 't5-large', 'text-to-text generation', 770, 'u5');
insert into model values('m6', 'clip-base', 'image-text embedding', 150, 'u6');
insert into model values('m7', 'llama-3', 'language generation', 70000, 'u7');

-- More files for each model
insert into file values('f3', '/nlp/bert-base/model.safetensors', 420, 'm2');
insert into file values('f4', '/nlp/bert-base/vocab.txt', 0.35, 'm2');

insert into file values('f5', '/vision/vit-large/model.safetensors', 1600, 'm3');
insert into file values('f6', '/vision/vit-large/config.json', 0.52, 'm3');

insert into file values('f7', '/asr/whisper-small/model.safetensors', 520, 'm4');
insert into file values('f8', '/asr/whisper-small/tokenizer.json', 0.98, 'm4');

insert into file values('f9', '/llm/t5-large/model.safetensors', 2900, 'm5');
insert into file values('f10', '/llm/t5-large/spiece.model', 0.76, 'm5');

insert into file values('f11', '/multimodal/clip-base/model.safetensors', 600, 'm6');
insert into file values('f12', '/multimodal/clip-base/config.json', 0.44, 'm6');

insert into file values('f13', '/llm/llama-3/model.safetensors', 82000, 'm7');
insert into file values('f14', '/llm/llama-3/tokenizer.json', 1.10, 'm7');

-- More download activity
insert into download values('u2', 'f3');
insert into download values('u2', 'f4');
insert into download values('u3', 'f5');
insert into download values('u3', 'f6');
insert into download values('u4', 'f7');
insert into download values('u4', 'f8');
insert into download values('u5', 'f9');
insert into download values('u5', 'f10');
insert into download values('u6', 'f11');
insert into download values('u6', 'f12');
insert into download values('u7', 'f13');
insert into download values('u7', 'f14');

-- Some cross-user downloads
insert into download values('u1', 'f3');
insert into download values('u2', 'f9');
insert into download values('u3', 'f11');
insert into download values('u4', 'f1');
insert into download values('u5', 'f5');
insert into download values('u6', 'f13');


-- add even more data
-- More users
insert into user values('u8', 'noah kim', 'noah@princeton.edu');
insert into user values('u9', 'olivia chen', 'olivia@cmu.edu');
insert into user values('u10', 'ethan brown', 'ethan@utoronto.ca');
insert into user values('u11', 'mia garcia', 'mia@ox.ac.uk');
insert into user values('u12', 'lucas martin', 'lucas@cam.ac.uk');
insert into user values('u13', 'ava lopez', 'ava@uw.edu');
insert into user values('u14', 'jackson lee', 'jackson@nyu.edu');
insert into user values('u15', 'zoe park', 'zoe@umich.edu');

-- More models
insert into model values('m8', 'resnet-50', 'image classification', 25.6, 'u8');
insert into model values('m9', 'wav2vec2-base', 'speech recognition', 95, 'u9');
insert into model values('m10', 'roberta-large', 'language understanding', 355, 'u10');
insert into model values('m11', 'detr-resnet', 'object detection', 41, 'u11');
insert into model values('m12', 'gpt-neo', 'language generation', 2700, 'u12');
insert into model values('m13', 'stable-diffusion', 'text-to-image', 8900, 'u13');
insert into model values('m14', 'segformer-b5', 'semantic segmentation', 84, 'u14');
insert into model values('m15', 'mistral-7b', 'language generation', 7000, 'u15');

-- More files
insert into file values('f15', '/vision/resnet-50/model.safetensors', 98, 'm8');
insert into file values('f16', '/vision/resnet-50/config.json', 0.42, 'm8');

insert into file values('f17', '/asr/wav2vec2-base/model.safetensors', 380, 'm9');
insert into file values('f18', '/asr/wav2vec2-base/tokenizer.json', 1.10, 'm9');

insert into file values('f19', '/nlp/roberta-large/model.safetensors', 1270, 'm10');
insert into file values('f20', '/nlp/roberta-large/vocab.json', 0.82, 'm10');

insert into file values('f21', '/vision/detr-resnet/model.safetensors', 410, 'm11');
insert into file values('f22', '/vision/detr-resnet/config.json', 0.55, 'm11');

insert into file values('f23', '/llm/gpt-neo/model.safetensors', 10200, 'm12');
insert into file values('f24', '/llm/gpt-neo/tokenizer.json', 1.22, 'm12');

insert into file values('f25', '/diffusion/stable-diffusion/model.safetensors', 12300, 'm13');
insert into file values('f26', '/diffusion/stable-diffusion/config.json', 0.92, 'm13');

insert into file values('f27', '/vision/segformer-b5/model.safetensors', 330, 'm14');
insert into file values('f28', '/vision/segformer-b5/config.json', 0.61, 'm14');

insert into file values('f29', '/llm/mistral-7b/model.safetensors', 13800, 'm15');
insert into file values('f30', '/llm/mistral-7b/tokenizer.json', 1.06, 'm15');

-- More downloads (mix of self and cross downloads)
insert into download values('u8', 'f15');
insert into download values('u8', 'f16');
insert into download values('u9', 'f17');
insert into download values('u9', 'f18');
insert into download values('u10', 'f19');
insert into download values('u10', 'f20');
insert into download values('u11', 'f21');
insert into download values('u11', 'f22');
insert into download values('u12', 'f23');
insert into download values('u12', 'f24');
insert into download values('u13', 'f25');
insert into download values('u13', 'f26');
insert into download values('u14', 'f27');
insert into download values('u14', 'f28');
insert into download values('u15', 'f29');
insert into download values('u15', 'f30');

-- Cross-user downloads
insert into download values('u1', 'f15');
insert into download values('u2', 'f19');
insert into download values('u3', 'f23');
insert into download values('u4', 'f25');
insert into download values('u5', 'f27');
insert into download values('u6', 'f29');
insert into download values('u7', 'f17');
insert into download values('u8', 'f13');
insert into download values('u9', 'f11');
insert into download values('u10', 'f9');
insert into download values('u11', 'f7');
insert into download values('u12', 'f5');
insert into download values('u13', 'f3');
insert into download values('u14', 'f1');
insert into download values('u15', 'f2');
insert into download values('u15', 'f11');

