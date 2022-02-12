import os
import json
import sys


def get_jars(minecraft_dir, version):
    jsonFilePath = minecraft_dir + '/versions/' + version + '/' + version + '.json'

    with open(jsonFilePath, 'r') as jsonFile:
        jsonFileContent = jsonFile.read()

    jsonFileKeys = json.loads(jsonFileContent)

    jars = ''
    for x in jsonFileKeys['libraries']:
        jarFileParts = x['name'].split(':')
        jarFile = minecraft_dir+'/libraries/' + \
            jarFileParts[0].replace('.', '/') + '/'+jarFileParts[1] + '/'+jarFileParts[2] + '/' + \
            jarFileParts[1] + '-'+jarFileParts[2] + '.jar'

        jars += jarFile+':'

    if 'inheritsFrom' in jsonFileKeys.keys():
        jars += get_jars(minecraft_dir, jsonFileKeys['inheritsFrom'])

    return jars


def get_offline_minecraft_argvs(minecraft_dir: str, version: str, player_name: str):
    """离线(非正版)登录"""
    jsonFilePath = minecraft_dir + '/versions/' + version + '/' + version + '.json'
    with open(jsonFilePath, 'r') as jsonFile:
        jsonFileContent = jsonFile.read()
    jsonFileKeys = json.loads(jsonFileContent)
    argvs = [
        "--username ${auth_player_name}",
        "--version ${version_name}"
        "--gameDir ${game_directory}",
        "--assetsDir ${assets_root}",
        "--assetIndex ${assets_index_name}",
        "--uuid ${auth_uuid}",
        "--accessToken ${auth_access_token}",
        "--userType ${user_type}",
        "--versionType ${version_type}"]
    argvs = " ".join(argvs)
    argvs = argvs.replace('${auth_player_name}', player_name)\
        .replace('${version_name}', 'QTML')\
        .replace('${game_directory}', minecraft_dir)\
        .replace('${assets_root}', minecraft_dir + '/assets')\
        .replace('${assets_index_name}', jsonFileKeys['assets'])\
        .replace('${auth_uuid}', '{}')\
        .replace('${auth_access_token}', '{}')\
        .replace('${user_type}', 'Legacy')\
        .replace('${version_type}', jsonFileKeys['type'])\
        .replace('${user_properties}', '{}')
    argvs = jsonFileKeys['mainClass'] + ' ' + argvs
    return argvs


def offline(minecraft_dir: str, minecraft_version: str, player_name: str, max_men: str, java_execfile: str):
    """离线(非正版)启动"""
    befour = f'{java_execfile} -Xincgc -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -Xmn128m -Xmx' + max_men + ' -Djava.library.path=' + minecraft_dir + \
        '/versions/' + minecraft_version + '/' + minecraft_version + \
        '-natives -Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true -Duser.home=/ -cp "'

    after = get_offline_minecraft_argvs(
        minecraft_dir, minecraft_version, player_name)

    jars = get_jars(minecraft_dir, minecraft_version)
    jars += minecraft_dir + '/versions/' + \
        minecraft_version + '/' + minecraft_version + '.jar" '

    cmd = befour + jars + after
    os.chdir(minecraft_dir)
    os.system(cmd)


if __name__ == "__main__":
    offline("E:/minecraft-java/.minecraft", "1.12.2", "mn2b", "10140m", "java")
