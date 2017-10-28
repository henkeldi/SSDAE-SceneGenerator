#version 450 core

layout (location=0) in vec3 position;

layout (binding=0) readonly buffer SCENE_BUFFER {
	mat4 view;
	mat4 projection;
	vec3 viewPos;
};

layout (binding=1) readonly buffer OBJECT_BUFFER {
	mat4 object[];
};

layout (location=0) uniform uint object_id = 0;

void main(){
	gl_Position = projection * view * object[object_id] * vec4(position, 1.0);
}