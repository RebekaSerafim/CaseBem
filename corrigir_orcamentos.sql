-- Script para corrigir os orçamentos órfãos
-- Deletar todos os orçamentos existentes (estão com IDs de demanda inválidos)
BEGIN TRANSACTION;

DELETE FROM item_orcamento;
DELETE FROM orcamento;

-- Recriar orçamentos com IDs corretos de demanda
-- Os IDs de demanda corretos são 128-151 (e demanda 7 que já existia)

-- Fornecedor Carlos Silva (id=2) - Fornece várias categorias
-- Demandas do Casal 1: 128, 129
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(128, 2, 'PENDENTE', 1800.00, 'Temos todo o mobiliário necessário para sua recepção', '2025-10-11 10:30:00'),
(129, 2, 'ACEITO', 2000.00, 'Mobiliário premium selecionado especialmente para vocês', '2025-10-11 11:15:00'),
(141, 2, 'PENDENTE', 3000.00, 'Estrutura reforçada para resistir ao vento da praia', '2025-10-11 14:20:00'),
(146, 2, 'PENDENTE', 2500.00, 'Móveis brancos coordenados conforme solicitado', '2025-10-11 15:45:00'),
(130, 2, 'PENDENTE', 650.00, 'Convites elegantes para casamento clássico', '2025-10-12 09:00:00'),
(147, 2, 'ACEITO', 800.00, 'Convites artesanais feitos à mão com papel reciclado', '2025-10-12 10:30:00'),
(129, 2, 'PENDENTE', 450.00, 'Convites e papelaria coordenada', '2025-10-12 11:00:00'),
(150, 2, 'PENDENTE', 1200.00, 'Convites de luxo com acabamento especial', '2025-10-12 14:00:00');

-- Fornecedor Ana Costa (id=3)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(130, 3, 'PENDENTE', 3000.00, 'Assessoria completa com nossa equipe experiente', '2025-10-11 09:00:00'),
(144, 3, 'ACEITO', 2500.00, 'Experiência em eventos grandes, tudo sob controle', '2025-10-11 10:00:00'),
(150, 3, 'PENDENTE', 3500.00, 'Cerimonial premium do início ao fim', '2025-10-11 11:30:00'),
(136, 3, 'PENDENTE', 15000.00, 'Buffet internacional de luxo com menu degustação', '2025-10-11 13:00:00'),
(133, 3, 'ACEITO', 7000.00, 'Buffet campestre gourmet com produtos regionais', '2025-10-11 14:30:00'),
(134, 3, 'PENDENTE', 9500.00, 'Buffet completo com estações e churrasco', '2025-10-11 15:00:00'),
(144, 3, 'PENDENTE', 10000.00, 'Buffet farto para 200 pessoas', '2025-10-11 16:00:00'),
(129, 3, 'REJEITADO', 3800.00, 'Bar premium com bebidas importadas', '2025-10-12 09:30:00');

-- Fornecedor Mariana Santos (id=4)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(150, 4, 'ACEITO', 550.00, 'Maquiagem e penteado com teste incluso', '2025-10-11 08:30:00'),
(151, 4, 'PENDENTE', 150.00, 'Prova de maquiagem antes do grande dia', '2025-10-11 09:00:00'),
(130, 4, 'PENDENTE', 5000.00, 'Vestido princesa sob medida com 3 provas', '2025-10-11 10:30:00'),
(136, 4, 'ACEITO', 8000.00, 'Vestido alta costura de designer renomado', '2025-10-11 11:00:00'),
(151, 4, 'PENDENTE', 8500.00, 'Vestido sob medida + ternos para padrinhos', '2025-10-11 13:00:00'),
(130, 4, 'PENDENTE', 350.00, 'Maquiagem profissional de noiva', '2025-10-12 09:00:00'),
(136, 4, 'PENDENTE', 500.00, 'Maquiagem e penteado de luxo', '2025-10-12 10:00:00'),
(144, 4, 'PENDENTE', 4500.00, 'Vestido tradicional elegante', '2025-10-12 11:00:00');

-- Fornecedor Pedro Oliveira (id=5)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(128, 5, 'ACEITO', 1500.00, 'Jardim perfeito para cerimônia intimista', '2025-10-11 08:00:00'),
(130, 5, 'PENDENTE', 800.00, 'Capela linda para cerimônia religiosa', '2025-10-11 09:00:00'),
(133, 5, 'PENDENTE', 2500.00, 'Sítio com vista maravilhosa para pôr do sol', '2025-10-11 10:00:00'),
(140, 5, 'ACEITO', 2000.00, 'Estrutura completa para casamento na praia', '2025-10-11 11:00:00'),
(144, 5, 'PENDENTE', 1000.00, 'Igreja ampla comporta até 250 pessoas', '2025-10-11 13:00:00'),
(147, 5, 'PENDENTE', 1800.00, 'Jardim natural estilo boho', '2025-10-11 14:00:00'),
(137, 5, 'PENDENTE', 5000.00, 'Pacote de hospedagem VIP 10 suítes', '2025-10-11 15:00:00'),
(150, 5, 'PENDENTE', 2500.00, 'Espaço para cerimônia no local', '2025-10-11 16:00:00');

-- Fornecedor Patricia Souza (id=6)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(130, 6, 'ACEITO', 1500.00, 'Alianças clássicas em ouro 18k', '2025-10-11 09:30:00'),
(136, 6, 'PENDENTE', 3000.00, 'Alianças com diamantes cravados', '2025-10-11 10:30:00'),
(150, 6, 'PENDENTE', 2500.00, 'Alianças elegantes com pedra', '2025-10-11 11:30:00'),
(151, 6, 'ACEITO', 1200.00, 'Brincos e colar de pérolas para noiva', '2025-10-11 13:00:00'),
(130, 6, 'PENDENTE', 1000.00, 'Alianças simples e elegantes', '2025-10-11 14:00:00'),
(129, 6, 'PENDENTE', 250.00, 'Tiara e brincos para noiva', '2025-10-11 15:00:00'),
(133, 6, 'PENDENTE', 1800.00, 'Alianças rústicas únicas', '2025-10-11 16:00:00'),
(144, 6, 'ACEITO', 1600.00, 'Conjunto completo de joias', '2025-10-12 09:00:00');

-- Fornecedor Julia Ferreira (id=7)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(135, 7, 'PENDENTE', 3500.00, 'Decoração de luxo com flores importadas', '2025-10-11 08:00:00'),
(136, 7, 'ACEITO', 3800.00, 'Flores exclusivas e decoração sofisticada', '2025-10-11 09:00:00'),
(133, 7, 'PENDENTE', 2500.00, 'Flores campestres e decoração rústica', '2025-10-11 10:00:00'),
(143, 7, 'PENDENTE', 2800.00, 'Decoração clássica com muitas flores brancas', '2025-10-11 11:00:00'),
(147, 7, 'ACEITO', 2200.00, 'Decoração boho com flores silvestres', '2025-10-11 13:00:00'),
(150, 7, 'PENDENTE', 3200.00, 'Decoração completa do espaço', '2025-10-11 14:00:00');

-- Fornecedor Fernanda Lima (id=8)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(132, 8, 'ACEITO', 4000.00, 'Fotografia e filmagem premium com drone', '2025-10-11 08:30:00'),
(135, 8, 'PENDENTE', 5000.00, 'Cobertura fotográfica de luxo com álbum', '2025-10-11 09:30:00'),
(142, 8, 'PENDENTE', 4500.00, 'Fotografia especializada em casamento de praia', '2025-10-11 10:30:00'),
(143, 8, 'ACEITO', 3800.00, 'Fotografia tradicional com vídeo', '2025-10-11 11:30:00'),
(147, 8, 'PENDENTE', 3500.00, 'Fotografia estilo boho com edição artística', '2025-10-11 13:00:00'),
(150, 8, 'PENDENTE', 4200.00, 'Cobertura completa foto e vídeo', '2025-10-11 14:00:00');

-- Fornecedor Roberto Almeida (id=9)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(129, 9, 'ACEITO', 2500.00, 'Música ao vivo com banda completa', '2025-10-11 08:00:00'),
(135, 9, 'PENDENTE', 3500.00, 'DJ profissional + som e iluminação de luxo', '2025-10-11 09:00:00'),
(139, 9, 'PENDENTE', 2000.00, 'DJ moderno para mini wedding', '2025-10-11 10:00:00'),
(147, 9, 'ACEITO', 1800.00, 'Música acústica ao vivo com violão', '2025-10-11 11:00:00'),
(148, 9, 'PENDENTE', 1500.00, 'Violão e voz para cerimônia', '2025-10-11 13:00:00'),
(150, 9, 'PENDENTE', 3000.00, 'Banda completa para festa', '2025-10-11 14:00:00');

-- Fornecedor Lucas Martins (id=10)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(132, 10, 'PENDENTE', 4000.00, 'Bolo de casamento 4 andares decorado', '2025-10-11 08:30:00'),
(135, 10, 'ACEITO', 5000.00, 'Bolo de luxo com decoração exclusiva', '2025-10-11 09:30:00'),
(139, 10, 'PENDENTE', 2500.00, 'Bolo moderno e elegante', '2025-10-11 10:30:00'),
(149, 10, 'PENDENTE', 3000.00, 'Mesa de doces artesanais gourmet', '2025-10-11 11:30:00'),
(146, 10, 'ACEITO', 1800.00, 'Bolo simples mas bonito', '2025-10-11 13:00:00'),
(150, 10, 'PENDENTE', 4500.00, 'Bolo e mesa de doces completa', '2025-10-11 14:00:00');

-- Fornecedora Beatriz Rocha (id=11)
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, status, valor_total, observacoes, data_hora_cadastro)
VALUES
(148, 11, 'ACEITO', 1500.00, 'Celebrante alternativo para cerimônia personalizada', '2025-10-11 08:00:00'),
(130, 11, 'PENDENTE', 1200.00, 'Celebrante para cerimônia religiosa', '2025-10-11 09:00:00'),
(143, 11, 'PENDENTE', 1300.00, 'Celebrante tradicional experiente', '2025-10-11 10:00:00'),
(135, 11, 'ACEITO', 2000.00, 'Celebrante de luxo com cerimônia exclusiva', '2025-10-11 11:00:00'),
(147, 11, 'PENDENTE', 1400.00, 'Celebrante para casamento boho', '2025-10-11 13:00:00'),
(150, 11, 'PENDENTE', 1600.00, 'Celebrante para cerimônia completa', '2025-10-11 14:00:00');

COMMIT;

-- Validação
SELECT 'Orçamentos criados:' as metrica, COUNT(*) as valor FROM orcamento
UNION ALL
SELECT 'Orçamentos órfãos:', COUNT(*) FROM orcamento o WHERE NOT EXISTS (SELECT 1 FROM demanda d WHERE d.id = o.id_demanda);
