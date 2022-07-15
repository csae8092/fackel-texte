<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0" exclude-result-prefixes="xsl tei xs">
    
    <xsl:template match="tei:person" name="person_detail">
        <xsl:param name="showNumberOfMentions" as="xs:integer" select="50000" />
        <xsl:variable name="selfLink">
            <xsl:value-of select="concat(data(@xml:id), '.html')"/>
        </xsl:variable>
        <div class="card-body">
            <ul>
                <li><small>geboren:</small>  <xsl:value-of select=".//tei:birth/tei:date/text()"/> <xsl:text> </xsl:text><xsl:value-of select=".//tei:birth/tei:place/text()"/></li>
                <li><small>gestorben:</small> <xsl:value-of select=".//tei:death/tei:date/text()"/> <xsl:text> </xsl:text><xsl:value-of select=".//tei:death/tei:place/text()"/></li>
                <xsl:if test=".//tei:idno">
                <li><small>URIs:</small>
                    <ul>
                        <xsl:for-each select=".//tei:idno">
                            <li>
                                <a>
                                    <xsl:attribute name="href"><xsl:value-of select="./text()"/></xsl:attribute>
                                    <xsl:value-of select="./text()"/>
                                </a>
                            </li>
                        </xsl:for-each>
                    </ul>
                </li>
                </xsl:if>
            </ul>

            
            
            
            
            <xsl:if test=".//tei:event">
                <div id="mentions">
                    <legend>erwähnt in</legend>
                    <ul>
                        <xsl:for-each select=".//tei:event">
                            <xsl:variable name="linkToDocument">
                                <xsl:value-of select="replace(tokenize(data(.//@target), '/')[last()], '.xml', '.html')"/>
                            </xsl:variable>
                            <li>
                                <xsl:value-of select=".//tei:title"/><xsl:text> </xsl:text>
                                <a href="{$linkToDocument}">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                            </li>
                        </xsl:for-each>
                    </ul>
                    
                </div>
            </xsl:if>
            
        </div>
    </xsl:template>
</xsl:stylesheet>