SELECT
    dados.ano as ano,
    dados.sigla_uf AS sigla_uf,
    diretorio_sigla_uf.nome AS sigla_uf_nome,
    dados.id_municipio AS id_municipio,
    diretorio_id_municipio.nome AS id_municipio_nome,
    dados.ibc as ibc,
    dados.cobertura_pop_4g5g as cobertura_pop_4g5g,
    dados.fibra as fibra,
    dados.densidade_smp as densidade_smp,
    dados.hhi_smp as hhi_smp,
    dados.densidade_scm as densidade_scm,
    dados.hhi_scm as hhi_scm,
    dados.adensamento_estacoes as adensamento_estacoes
FROM `basedosdados.br_anatel_indice_brasileiro_conectividade.municipio` AS dados
LEFT JOIN (SELECT DISTINCT sigla,nome  FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
    ON dados.sigla_uf = diretorio_sigla_uf.sigla
LEFT JOIN (SELECT DISTINCT id_municipio,nome  FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio
    ON dados.id_municipio = diretorio_id_municipio.id_municipio